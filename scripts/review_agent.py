import os
import json
import requests
import sys

# --- CONFIGURATION FOR KODEKEY ---
API_KEY = os.getenv("GOOGLE_API_KEY") # We keep the var name same for convenience
# KodeKey uses OpenAI-compatible endpoints
API_URL = "https://kodekey.ai.kodekloud.com/v1/chat/completions"
# We use a standard model supported by KodeKey
MODEL = "anthropic/claude-sonnet-4" 

def ask_ai(violations):
    if not API_KEY:
        print("❌ Error: API Key is missing. Run 'export GOOGLE_API_KEY=...'")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 1. System Prompt
    system_instruction = """
    You are a Cloud Security Expert. Review these Terraform violations.
    
    CRITICAL RULES:
    1. If 'EC2LabRole' is found -> REJECT immediately (Privilege Escalation).
    2. If HIGH severity issues exist -> REJECT.
    3. If only LOW/MEDIUM issues -> SUGGEST FIXES but APPROVE.
    
    Respond in this format:
    - SUMMARY: (One line summary)
    - RISK ASSESSMENT: (Why is this bad?)
    - ACTION: (APPROVE or REJECT)
    """

    # 2. Construct Payload (OpenAI Format)
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"VIOLATIONS DETECTED:\n{json.dumps(violations, indent=2)}"}
        ],
        "temperature": 0.2
    }
    
    try:
        # 3. Send Request
        response = requests.post(API_URL, headers=headers, json=data)
        
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

        result = response.json()
        
        # 4. Parse Response (OpenAI Format)
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            print(f"⚠️ API returned empty choices: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Connection Exception: {str(e)}")
        return None

def main():
    # 1. Check if scan results exist
    scan_file = "scan_results.json"
    if not os.path.exists(scan_file):
        print(f"⚠️ No scan file found at {scan_file}. Assuming clean scan.")
        sys.exit(0)

    # 2. Read the scan results
    try:
        with open(scan_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Error: scan_results.json is not valid JSON.")
        sys.exit(1)

    # 3. Extract violations
    violations = data.get("results", {}).get("violations", [])
    
    if not violations:
        print("✅ No violations found. Security check passed!")
        sys.exit(0)

    print(f"🔍 Found {len(violations)} violations. Consulting AI Agent...")

    # 4. Ask The AI
    ai_review = ask_ai(violations)

    if ai_review:
        print("\n" + "="*40)
        print("🤖 AI SECURITY REVIEW")
        print("="*40 + "\n")
        print(ai_review)
        print("\n" + "="*40)
        
        if "REJECT" in ai_review:
            print("❌ AI has REJECTED this Pull Request.")
            sys.exit(1)
        else:
            print("✅ AI has APPROVED this Pull Request.")
            sys.exit(0)
    else:
        print("❌ Failed to get AI review. Failing pipeline.")
        sys.exit(1)

if __name__ == "__main__":
    main()