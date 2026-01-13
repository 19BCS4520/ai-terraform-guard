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
    
    # We teach Gemini to be strict about Lab Roles
    prompt = f"""
    You are a Cloud Security Expert. Review these Terraform violations.

    CRITICAL RULES:
    1. If 'EC2LabRole' is found -> REJECT immediately (Privilege Escalation Risk).
    2. If port 22 is open to 0.0.0.0/0 -> REJECT immediately.
    3. If 'AdministratorAccess' policy is used -> REJECT.
    
    VIOLATIONS FOUND:
    {json.dumps(violations, indent=2)}
    
    OUTPUT FORMAT:
    Reply strictly with a JSON object: {{ "verdict": "APPROVE" or "REJECT", "reason": "One sentence explanation" }}
    """

    payload = { "contents": [{ "parts": [{"text": prompt}] }] }
    
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        # Clean up response to ensure valid JSON
        text_resp = resp.json()['candidates'][0]['content']['parts'][0]['text']
        clean_json = text_resp.replace('```json','').replace('```','').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"AI Connection Error: {e}")
        sys.exit(1)

def main():
    if not os.path.exists(SCAN_FILE):
        print("No scan file found.")
        sys.exit(0)
        
    with open(SCAN_FILE) as f:
        data = json.load(f)

    violations = data.get('results', {}).get('violations', [])
    
    if not violations:
        print("✅ No violations found. Approved.")
        sys.exit(0)

    print(f"⚠️ Found {len(violations)} violations. Consulting Gemini...")
    decision = ask_gemini(violations)
    
    print(f"\n📢 AI VERDICT: {decision['verdict']}")
    print(f"📝 REASON: {decision['reason']}\n")
    
    if decision['verdict'] == "REJECT":
        sys.exit(1) # Fails the pipeline

if __name__ == "__main__":
    main()