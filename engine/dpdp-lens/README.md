# DPDP Lens – AI-Assisted Privacy Policy Compliance Assessment

**Academic Prototype | Preliminary Policy Assessment | Not Legal Advice**

---

## What is this?

DPDP Lens is a simple academic prototype that helps assess a privacy policy PDF
against a selected set of requirements from the **Digital Personal Data Protection
(DPDP) Act 2023** and **DPDP Rules 2025**.

Built as an MLIS/MCLIS academic demonstration project.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Configure AI key

Copy `.env.example` to `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

Without a key, the app runs in **Demo Mode** using keyword-based analysis.

### 3. Create the sample PDF (first time only)

```bash
python create_sample_pdf.py
```

### 4. Run the application

```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`.

---

## How to use

1. **Upload** a privacy policy PDF using the file uploader.
2. Click **"Analyse Policy"**.
3. Wait for the analysis to complete (10 requirements checked).
4. View the **Summary**, **Readiness Score**, and **Detailed Results**.
5. **Download** the HTML report.

For a demo, use `sample/sample_privacy_policy.pdf`.

---

## Project Structure

```
dpdp-lens/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── create_sample_pdf.py    ← One-time script to generate sample PDF
├── .env.example            ← API key template
├── README.md               ← This file
├── data/
│   └── requirements.json   ← DPDP Act requirements for assessment
└── sample/
    └── sample_privacy_policy.pdf  ← Sample policy for demonstration
```

---

## Assessment Requirements Covered

| ID  | Requirement                       | Legal Source                |
|-----|-----------------------------------|-----------------------------|
| R01 | Notice to Data Principals         | DPDP Act 2023, Section 5    |
| R02 | Purpose of Processing             | DPDP Act 2023, Section 6–7  |
| R03 | Types of Personal Data Collected  | DPDP Act 2023, Section 5(1) |
| R04 | Consent Mechanism                 | DPDP Act 2023, Section 6    |
| R05 | Data Principal Rights             | DPDP Act 2023, Sections 11–14 |
| R06 | Data Retention and Erasure        | DPDP Act 2023, Section 8(7) |
| R07 | Security Safeguards               | DPDP Act 2023, Section 8(5) |
| R08 | Data Sharing / Third Parties      | DPDP Act 2023, Section 8–9  |
| R09 | Grievance Redressal               | DPDP Act 2023, Section 13   |
| R10 | Children's Personal Data          | DPDP Act 2023, Section 9    |

---

## Scoring

| Status              | Points |
|---------------------|--------|
| Addressed           | 100    |
| Partially Addressed | 50     |
| Potential Gap       | 0      |

**Preliminary Readiness Score** = Average of all requirement scores.

> This score represents policy coverage within the selected prototype requirements.
> It is **not** a legal compliance score.

---

## Important Disclaimers

- This application is an **academic prototype**.
- Results are **preliminary assessments** only.
- This is **not legal advice** and **not a compliance certification**.
- The application does **not** certify any organisation as legally compliant or non-compliant.
- AI-generated results should be reviewed by a qualified legal professional.
