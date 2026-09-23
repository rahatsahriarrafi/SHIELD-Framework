# SHIELD V5 — Proposed Target Architecture

> New Telecom Ltd | Robi Data Privacy Avengers | Privacy without friction

This is the master control list (V5). Demos in `/demos` prove the AI technical core; this document covers the full PDPA operating model.

## Architecture
Zero Trust (ZTNA, microsegmentation, NGFW) · isolated HA AI zone (segmented from billing/subscriber) · mTLS in AI pipeline · AI-zone DR/BCP with fail-closed for critical AI · AI kill switch · VPN as MFA- and posture-protected backup only

## Access
ABAC (purpose-bound) + JIT/PAM · phishing-resistant MFA (FIDO2; no SMS-only OTP for privileged) · biometric only where justified · human-in-the-loop with defined thresholds · risk-based step-up for customers · UEBA for privileged AI/data access

## Database
TLS/mTLS · TDE · field encryption · tokenization · KMS/HSM (rotation, SoD) · field-level residency tagging / lineage

## AI tech
Hardened RAG · Presidio-style BD NID/phone/Bangla/eKYC redaction · prompt behaviour analysis + output guardrails · query rate-limit/anomaly detection · Differential Privacy with written ε policy (≈1.0) · SHAP for scoring models · citations + stored decision logs for LLMs · bias testing · model cards · drift monitoring · versioning & rollback · re-approval on change · signed model artifacts in CI/CD · tested against OWASP LLM Top 10 and MITRE ATLAS · StruQ-style separation on roadmap

## Customer trust & experience
Reason codes · fast human review for fraud blocks with temporary-release path + proactive SMS · appeal channel · AI disclosure with human handoff after failed turns · Bangla, English, Banglish · privacy dashboard plus USSD/IVR/SMS/retail · layered notices · granular per-AI-use-case consent · no dark patterns · no service penalty for opt-out · DSAR SLAs with status tracking · privacy complaint and escalation · remediation policy · vulnerable-customer handling · customer-facing transparency on vendors and cross-border transfers · parent/guardian guidance · usability testing and VoC loop · customer KPIs (CSAT, trust score, false-positive rate, DSAR/appeal SLA) · framing: **privacy without friction**

## Children's protection
Age assurance (prefer existing registration/payment data) · no profiling if age uncertain · under-18 suppression in marketing and churn · misclassification correction · periodic audits

## Data lifecycle
Minimization · retention and auto-deletion (prompts, embeddings, logs, training sets) · vector DB deletion for DSARs · retrain policy for erasure · automated discovery · app-to-data inventory

## Incident
AI-aware breach playbook · regulator/customer/employee notification within PDPA timelines · plain-language notice from verified sender IDs · helpline + remediation

## Assurance
VAPT · AI red teaming · SIEM · WORM logs (fixed retention, no PII) · internal audit · mock PDPA audit · evidence repository · bug bounty (AI tier) · vendor SOC 2 / ISO 27001 / ISO 42001 gates · aligned to ISO 42001 & ISO 27701

## Employee & non-prod
HR data under PDPA controls · masked or synthetic data only in non-production

## Supply chain & third parties
AIBOM and provenance · signed/checksummed models · no training on our data · vendor tiering and register · DPAs · exit and deletion · egress monitoring · cross-border transfer register · in-country processing by default

## Governance
Independent DPO (veto) + AI & Privacy Council + RACI · CDO for data quality · RoPA · AI register · DPIA/PAIA + CI/CD gate · legal-basis register and consent · DSAR workflow · awareness for employees, vendors, and customers · roadmap and KPIs (audit-readiness % + customer KPIs)

## Not using
Blockchain for personal data (erasure conflict) · MAC address as authentication · keyword-only filters · SMS-only OTP for privileged access · public GenAI with customer/employee data (DLP/CASB blocked) · raw production data in non-production · dark-pattern consent · app-only privacy channels
