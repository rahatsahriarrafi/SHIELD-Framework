# SHIELD Framework

Secure, Hardened, Integrity, Explainable, Lawful, Defended

New Telecom Ltd case study for the Robi Data Privacy Avengers competition.

SHIELD is a practical framework for adopting telecom AI under Bangladesh’s Personal Data Protection Act, 2026. The idea is simple: protect people strongly, keep the experience easy (privacy without friction), and prove the technical pieces with runnable demos.

What you will find here:

- A one-page concept paper and a full proposed architecture
- Demo A: differential privacy and SHAP for churn and fraud style models
- Demo B: a hardened customer-support retrieval assistant with Bangladesh-aware PII checks

## What SHIELD adds beyond a demo alone

Many AI privacy demos stop at a model notebook. SHIELD also covers children’s PDPA rules, customer reason codes and appeals, inclusive channels such as USSD and IVR, Bangladesh identifier formats, and clear accountability through a data protection officer and an AI and Privacy Council.

## Repository structure

```
SHIELD-Framework/
├── README.md
├── requirements.txt
├── LICENSE
├── docs/
│   ├── SHIELD_Architecture.md
│   └── TeamNullX_ConceptPaper.pdf
├── demos/
│   ├── demo_a_dp_shap.py
│   └── demo_b_hardened_rag.py
├── notebooks/
└── images/
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python demos/demo_a_dp_shap.py
python demos/demo_b_hardened_rag.py
```

Plots are written to `images/`.

## Demo A: Privacy-preserving and explainable AI

This demo asks two questions. First, can we train on customer-like data without memorising individuals? We use a differential privacy style budget for that. Second, can we explain a high-risk decision? We use SHAP for specialists and plain reason codes for customers.

Method: compare a normal logistic regression baseline with an epsilon-calibrated private variant across epsilon values from 0.1 to 50. SHIELD’s working target is about epsilon = 1.0. In production you would swap in a full DP-SGD stack where needed.

### Results

Privacy and utility trade-off (lower epsilon means stronger privacy; the red line is the SHIELD target near 1.0):

![Privacy utility trade-off](images/shield_privacy_utility.png)

Churn versus fraud accuracy across privacy budgets:

![Accuracy comparison](images/shield_comparison_accuracy.png)

SHAP global drivers for churn:

![SHAP churn global](images/shield_shap_churn_global.png)

SHAP per-customer drivers for churn (useful for reason codes and appeals):

![SHAP churn customer](images/shield_shap_churn_customer.png)

SHAP global drivers for fraud:

![SHAP fraud global](images/shield_shap_fraud_global.png)

SHAP per-customer drivers for fraud:

![SHAP fraud customer](images/shield_shap_fraud_customer.png)

By default the demos use synthetic telco and fraud style data so they always run. You can drop your own CSV files into `data/` if you want.

## Demo B: Hardened RAG customer support

Every query goes through a short pipeline before it can touch the knowledge base:

1. Redact Bangladesh-style PII such as NID and phone numbers  
2. Check behaviour and known injection patterns  
3. Apply a rate and exfiltration anomaly guard  
4. Retrieve an answer, or block and send the case to human review  

This is stronger than keyword-only filters. It also tells the customer how to reach a human agent and includes PDPA-aware answers on opt-out, children’s rules, and appeals.

### Pipeline

![SHIELD Hardened RAG pipeline](images/shield_pipeline.png)

### PII redaction (BD NID and phone)

![PII redaction before and after](images/shield_pii_redaction.png)

### Test results

Legitimate answers versus injection or anomaly blocks:

![RAG test results](images/shield_rag_test_results.png)

## OWASP LLM and ATLAS alignment

| Risk | ID | SHIELD control | Demo |
|---|---|---|---|
| Prompt injection | LLM01 | Behaviour and pattern checks, anomaly guard, human review | B |
| Sensitive disclosure | LLM02 | Bangladesh-localised PII redaction before retrieve or log | B |
| Training-data leakage | - | Differential privacy budget | A |
| Opaque or unfair decisions | - | SHAP, reason codes, appeal path | A and docs |
| Supply chain | - | Model inventory, signed artefacts, no training on our data | docs |

The architecture also points to MITRE ATLAS style adversarial testing alongside normal VAPT and AI red teaming.

## Proposed target architecture

Full detail: [docs/SHIELD_Architecture.md](docs/SHIELD_Architecture.md)

In short, SHIELD combines Zero Trust networking, an isolated AI zone, purpose-bound access, encrypted data stores, hardened RAG, differential privacy and SHAP, customer-friendly recourse (including USSD and IVR), children’s PDPA controls, and governance with an independent data protection officer. We do not use blockchain for personal data, and we do not send live personal data into public generative AI tools.

## Competition artifact

Concept paper (one A4 page): [docs/TeamNullX_ConceptPaper.pdf](docs/TeamNullX_ConceptPaper.pdf)

## Research and standards (selected)

1. Abadi et al. (2016). Deep Learning with Differential Privacy. ACM CCS.  
2. Lundberg and Lee (2017). A Unified Approach to Interpreting Model Predictions. NeurIPS.  
3. Greshake et al. (2023). Prompt injection against LLM-integrated applications. AISec at CCS.  
4. Chen et al. (2025). StruQ structured queries against prompt injection. USENIX Security (roadmap item).  
5. OWASP Top 10 for Large Language Model Applications (2025).  
6. ISO/IEC 42001 and ISO/IEC 27701 as alignment targets.  
7. Bangladesh Personal Data Protection Act, 2026 (PDPA).

## Team

Built for the Robi Data Privacy Avengers competition (New Telecom Ltd case).  
Framework name: SHIELD. Guiding idea: privacy without friction.

## License

MIT. See `LICENSE`.
