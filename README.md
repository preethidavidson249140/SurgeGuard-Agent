
# SurgeGuard-Agent

**Consent-Aware Security Monitoring for Healthcare AI Workflows**

An educational healthcare workflow prototype combining simulated surgical risk monitoring, inventory management, and patient consent verification.

## Live Demo

https://surgeguard-agent-bafgymxyjjjd5vmctrbmo3.streamlit.app/

## Project Features

- Simulated surgical movement and sensor monitoring
- Inventory availability and stock forecasting
- Patient identifier verification
- Consent scope and expiry verification
- ALLOW/BLOCK security decisions
- Session-level security audit log and CSV export
- Healthcare simulation and security evaluation reports

## Technology Stack

- Python
- Streamlit
- Visual Studio Code
- Dify (used during workflow prototyping)

The deployed demonstration can operate using local rule-based logic without a Dify API key.

## Installation

Clone the repository:

```bash
git clone https://github.com/preethidavidson249140/SurgeGuard-Agent.git
cd SurgeGuard-Agent
```

Install the required packages:

```bash
pip install streamlit pandas requests
```

Run the dashboard:

```bash
streamlit run app.py
```

## Reproduce Security Evaluation

Run:

```bash
python test_security.py
```

The five tests cover:

1. Valid consent — ALLOW
2. Patient identifier mismatch — BLOCK
3. Unauthorised consent scope — BLOCK
4. Expired consent — BLOCK
5. Untrusted instruction accompanying an unauthorised request — BLOCK

Expected result: **5/5 tests pass**.

The evaluation script exports `SurgeGuard_Security_Evaluation.csv`.

## Healthcare Simulation Evaluation

Four selected scenarios were tested:

- Normal sensor and sufficient stock
- Abnormal sensor and sufficient stock
- Normal sensor and low stock
- Abnormal sensor and low stock

Results are recorded in `SurgeGuard_Simulation_Report.csv`.

## Combined Evaluation

Run:

```bash
python combine_reports.py
```

This combines the healthcare and security evaluation CSV files into `SurgeGuard_Combined_Evaluation.csv`.

Expected result: **9 records**.

## Security Architecture

The `security_guard.py` module checks:

- Patient identifier consistency
- Requested data scope against consent
- Consent expiry

It returns ALLOW only when all configured checks pass. Otherwise, it returns BLOCK with reasons.

## Limitations

This is an educational, rule-based prototype.

- No real patient information is used.
- No live ABDM or ABHA integration exists.
- No clinical validation has been performed.
- The security rules assume trusted consent metadata.
- Comprehensive adversarial testing and production-grade authentication are not implemented.
- Passing five selected tests does not establish real-world security effectiveness.

## SAFL Hackathon

- Track: Technical
- Challenge Area: Trust & Consent
- Participation: Online only

## Developer

Preethi Davidson  
Second-Year B.Sc. Computer Science with Artificial Intelligence  
SDNB Vaishnav College for Women
chennai