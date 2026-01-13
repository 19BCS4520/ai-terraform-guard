import os
import json
import requests
import sys

# CONFIGURATION
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SCAN_FILE = "scan_results.json"
MODEL = "gemini-1.5-flash"

def ask_gemini(violations):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # 1. Improved Prompt for the Demo
    prompt = f"""
    You are a Cloud Security Expert. Review these Terraform violations.
    
    CRITICAL RULES:
    1. If 'EC2LabRole' is found -> REJECT immediately (Privilege Escalation).
    2. If HIGH severity issues exist -> REJECT.
    3. If only LOW/MEDIUM issues -> SUGGEST FIXES but APPROVE.
    
    VIOLATIONS DETECTED:
    {json.dumps(violations, indent=2)}
    
    Respond in this format:
    - SUMMARY: (One line summary)
    - RISK ASSESSMENT: (Why is this bad?)
    - ACTION: (APPROVE or REJECT)
    """
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # 2. Check for API Errors (The Fix)
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

        result = response.json()
        
        # 3. Safely access the response
        if "candidates" in result and result["candidates"]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"⚠️ API returned 200 but no text (Safety Block?): {result}")
            return "Block: AI refused to review due to safety settings."
            
    except Exception as e:
        print(f"❌ Connection Exception: {str(e)}")
        return None

# --- ADDED MISSING MAIN FUNCTION ---
def main():
    # 1. Check if scan results exist
    if not os.path.exists(SCAN_FILE):
        print(f"⚠️ No scan file found at {SCAN_FILE}. Assuming clean scan.")
        sys.exit(0)

    # 2. Read the scan results
    try:
        with open(SCAN_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Error: scan_results.json is not valid JSON.")
        sys.exit(1)

    # 3. Extract violations (Adjust key based on your scanner: 'violations' vs 'results')
    violations = data.get("results", {}).get("violations", [])
    
    if not violations:
        print("✅ No violations found. Security check passed!")
        sys.exit(0)

    print(f"🔍 Found {len(violations)} violations. Consulting Gemini...")

    # 4. Ask Gemini
    ai_review = ask_gemini(violations)

    if ai_review:
        print("\n" + "="*40)
        print("🤖 GEMINI AI SECURITY REVIEW")
        print("="*40 + "\n")
        print(ai_review)
        print("\n" + "="*40)
        
        # 5. Fail the pipeline if the AI rejects the PR
        if "REJECT" in ai_review:
            print("❌ AI has REJECTED this Pull Request due to security risks.")
            sys.exit(1)
        else:
            print("✅ AI has APPROVED this Pull Request (with warnings).")
            sys.exit(0)
    else:
        print("❌ Failed to get AI review. Failing pipeline for safety.")
        sys.exit(1)

if __name__ == "__main__":
    main()