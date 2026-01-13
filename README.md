# 🛡️ AI-Terraform-Guard: Intelligent DevSecOps Pipeline

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-blue?logo=github-actions)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)
![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)
![Security](https://img.shields.io/badge/Security-AI_Powered-red)

An automated **DevSecOps pipeline** that acts as an intelligent security gatekeeper for Infrastructure as Code (IaC). 

Instead of relying solely on static rules, this project integrates **Generative AI** to analyze Terraform violations, assess real-world risk, and block insecure Pull Requests before they merge into production.

---

## 🚀 How It Works



1.  **Developer Pushes Code:** A user commits Terraform changes (e.g., creating an S3 bucket) to a feature branch.
2.  **Static Analysis (Terrascan):** The GitHub Actions workflow scans the code for known vulnerabilities and generates a JSON report.
3.  **AI Risk Assessment:** A Python agent parses the report and sends the violations to an **LLM (Large Language Model)** acting as a Cloud Security Expert.
4.  **Decision Engine:**
    * **CRITICAL/HIGH Risk:** The AI rejects the PR and provides a remediation plan.
    * **LOW Risk:** The AI warns the user but allows the merge.
    * **False Positives:** The AI can differentiate between intended configurations and actual threats.
5.  **Feedback Loop:** The AI blocks the merge and logs the rejection reason in the pipeline.

---

## 🧪 Tested Scenarios

This pipeline has been validated against real-world industry attack vectors. Below is a brief explanation of each test case:

### 1. The "Data Leak" (Public S3 Bucket)
* **The Attack:** A developer accidentally sets an S3 bucket ACL to `public-read` while tagging the data as "Confidential."
* **Why It Matters:** This is the #1 cause of cloud data breaches. It allows anyone on the internet to list and download files.
* **AI Verdict:** **REJECT**. The AI correlates the `public-read` setting with the `Confidential` tag, identifies the conflict, and blocks deployment to prevent immediate data exfiltration.

### 2. The "Wide Open Door" (Insecure Security Group)
* **The Attack:** A Security Group is configured to allow inbound traffic on Port 22 (SSH) from `0.0.0.0/0` (Anywhere).
* **Why It Matters:** Leaving SSH open to the world invites botnets to launch brute-force password attacks against the server.
* **AI Verdict:** **REJECT**. The AI flags this as a "High Severity" network risk, noting that management ports should only be accessible from specific, trusted IP ranges (VPNs).

### 3. The "Crown Jewels" (Exposed Database)
* **The Attack:** A production RDS database is deployed with `publicly_accessible = true`, storage unencrypted, and a hardcoded weak password.
* **Why It Matters:** This represents a catastrophic failure. It violates major compliance standards (GDPR, HIPAA, PCI-DSS) and exposes the core of the business to theft.
* **AI Verdict:** **CRITICAL REJECTION**. The AI identifies multiple compounded risks and explicitly blocks the merge due to "Compliance Violation" and "Data Sovereignty Risk."

### 4. Privilege Escalation (Custom Policy Enforcement)
* **The Attack:** A user attempts to create an IAM Role named `EC2LabRole` attached to `AdministratorAccess`.
* **Why It Matters:** Malicious insiders often create "innocent-sounding" roles to grant themselves Admin privileges later (Privilege Escalation).
* **AI Verdict:** **BLOCK**. The AI Agent was given a custom system prompt to specifically watch for the `EC2LabRole`. It detects the pattern and blocks it immediately, demonstrating the ability to enforce organization-specific policies.

---

## 📂 Project Structure

```bash
.
├── .github/workflows/   # CI/CD Pipeline definitions
│   └── security.yml     # The main workflow file
├── infrastructure/      # Terraform files (IaC)
├── scripts/             # Python logic
│   └── review_agent.py  # The AI Security Agent
├── scan_results.json    # (Artifact) Generated during runtime
└── README.md
