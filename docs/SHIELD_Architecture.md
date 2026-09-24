# SHIELD: Proposed Target Architecture

New Telecom Ltd | Robi Data Privacy Avengers | Privacy without friction

This document describes the full operating model we propose under PDPA. The demos in `/demos` show the AI technical core. Everything below is the wider control set that makes those demos safe to run in a real telecom setting.

## Architecture

We recommend Zero Trust using ZTNA, microsegmentation and a next-generation firewall. AI systems sit in an isolated, highly available zone kept apart from billing and subscriber cores. Traffic inside the AI pipeline uses mutual TLS. Critical AI should fail closed during recovery, with a documented kill switch. VPN remains only as a backup path that still requires MFA and device posture checks.

## Access

Access is purpose-bound through attribute-based controls, with just-in-time privileged access for administrators and data scientists. Staff use phishing-resistant MFA such as FIDO2. SMS-only OTP is not enough for privileged roles. Biometrics are used only where justified, with consent and careful template handling. High-impact AI decisions require human review against clear thresholds. Customer authentication should step up based on risk rather than constant friction. Privileged AI and data access is watched with behaviour analytics.

## Database and data protection

Personal data is protected with TLS or mTLS in transit, encryption at rest, field-level encryption for sensitive identifiers, tokenisation where useful, and keys held in a KMS or HSM with rotation and separation of duties. Field-level residency tagging helps answer where a record is stored and whether it leaves Bangladesh.

## AI technology

Customer support uses a hardened retrieval assistant with Bangladesh-aware redaction for NID, phone numbers and related identifiers, prompt behaviour analysis, output guardrails, and query rate or anomaly checks. Fraud and churn style models use differential privacy with a written epsilon policy (working target near 1.0). Scoring models are explained with SHAP. Large language paths keep citations and stored decision logs. The lifecycle includes bias testing, model cards, drift monitoring, versioning, rollback, re-approval on major change, signed artefacts in CI/CD, and testing against the OWASP LLM Top 10 and MITRE ATLAS. Structured prompt and user separation (StruQ style) is on the roadmap.

## Customer trust and experience

Customers should receive plain reason codes for adverse decisions. Fraud blocks should favour step-up checks or fast human review, with a temporary release path and a proactive SMS where appropriate. Appeals must be available. AI chats must say they are AI and hand off to a person after failed turns. Support should work in Bangla, English and mixed language. Privacy choices should work through a dashboard and also USSD, IVR, SMS and retail points. Notices should be layered and clear. Consent should be granular per use case, without dark patterns and without cutting core service when someone opts out. Data requests need SLAs and status tracking. Complaints need escalation. When the company is wrong, remediation should be defined. Vulnerable customers need assisted paths. Customers should also see, in plain language, which kinds of vendors receive data and whether it leaves Bangladesh. Parents need guidance on children’s SIM use. We test notices and flows with real users and track CSAT, trust, false-positive rate and request handling times. The guiding idea is privacy without friction.

## Children's protection

Age assurance should use data already held where possible, such as registration and payment signals. If age is uncertain, treat the person as a child and do not profile. Under-eighteens are kept out of marketing and churn behavioural models. There must be a simple route to correct misclassification, plus periodic audits.

## Data lifecycle

Collect only what is needed. Keep retention schedules and auto-delete prompts, embeddings, logs and training sets when they are no longer required. Vector databases must support deletion for data-subject requests. Erasure may require model retrain or refresh. Automated discovery and an application-to-data inventory keep the picture current.

## Incident response

Use an AI-aware breach playbook covering injection leaks, chatbot exposure, model or vector store incidents and vendor AI failures. Notify the regulator, customers and affected employees within PDPA timelines. Messages should be plain language, sent from verified sender IDs, with a helpline and remediation support.

## Assurance

Combine classical VAPT with AI red teaming, SIEM monitoring, WORM or tamper-evident logs that keep PII out and have fixed retention, internal audit, a mock PDPA audit, an evidence repository, and a bug bounty that includes AI issues. Prefer vendors with strong certifications such as SOC 2, ISO 27001 and ISO 42001. Align the programme to ISO 42001 and ISO 27701.

## Employee data and non-production

Employee and HR data receive the same PDPA-grade care as customer data. Development and test environments use masked or synthetic data only.

## Supply chain and third parties

Keep an AI bill of materials and provenance for models and libraries. Prefer signed and checksummed artefacts. Contracts must ban training on New Telecom data, set tiers, include data processing agreements, exit and deletion duties, egress monitoring, a cross-border transfer register, and in-country processing by default.

## Governance

An independent data protection officer can stop high-risk launches. An AI and Privacy Council and a clear RACI assign accountability. A chief data officer owns data quality. Maintain a record of processing, an AI register, privacy and AI impact assessments with a CI/CD gate, a legal-basis register, consent where required, data-subject request workflows, awareness for employees, vendors and customers, and a roadmap with both audit-readiness and customer outcome measures.

## What we do not use

We do not store personal data on a blockchain (it conflicts with correction and erasure). We do not use MAC address as login. We do not rely on keyword-only prompt filters. We do not accept SMS-only OTP for privileged access. We do not send customer or employee personal data into public generative AI tools, and we block that path technically. We do not put raw production data into non-production environments. We do not use dark-pattern consent or app-only privacy channels.
