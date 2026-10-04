"""
DPDP Lens – AI-Assisted Privacy Policy Compliance Assessment
============================================================
Academic Prototype | Preliminary Policy Assessment
Not Legal Advice | Not a Compliance Certification
"""

import os
import json
import re
import datetime
import streamlit as st

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DPDP Lens – Privacy Policy Assessment",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load .env if present ──────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Constants ─────────────────────────────────────────────────────────────────
SCORING    = {"Addressed": 100, "Partially Addressed": 50, "Potential Gap": 0}
RISK_MAP   = {"Addressed": "Low", "Partially Addressed": "Moderate", "Potential Gap": "High"}
STATUS_EMOJI = {
    "Addressed":           "✅ Addressed",
    "Partially Addressed": "⚠️ Partially Addressed",
    "Potential Gap":       "🔴 Potential Gap",
}
DISCLAIMER = (
    "Academic Prototype — Preliminary Policy Assessment — "
    "Not Legal Advice or Compliance Certification."
)

# ── Load requirements ─────────────────────────────────────────────────────────
@st.cache_data
def load_requirements():
    path = os.path.join(os.path.dirname(__file__), "data", "requirements.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ── PDF extraction ────────────────────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file):
    try:
        import pymupdf as fitz
        data = uploaded_file.read()
        doc  = fitz.open(stream=data, filetype="pdf")
        pages = doc.page_count
        text  = "\n".join(p.get_text() for p in doc)
        doc.close()
        return text, pages, None
    except ImportError:
        return None, 0, "PyMuPDF not installed. Run: python -m pip install pymupdf"
    except Exception as e:
        return None, 0, f"PDF read error: {e}"

# ── API key detection ─────────────────────────────────────────────────────────
def get_api_key():
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

# ── AI analysis (Gemini via google-genai SDK) ────────────────────────────────
def analyse_with_gemini(policy_text, req):
    from google import genai
    client  = genai.Client(api_key=get_api_key())
    excerpt = policy_text[:6000]
    prompt  = f"""You are an academic research assistant assessing a privacy policy.
This is NOT legal advice. This is an academic prototype.

REQUIREMENT:
ID: {req['id']} | {req['title']}
Description: {req['description']}
Assessment Question: {req['assessment_question']}
Legal Source: {req['legal_source']}

POLICY TEXT (excerpt):
{excerpt}

TASK: Return ONLY a valid JSON object with these exact keys:
- status: one of "Addressed", "Partially Addressed", or "Potential Gap"
- evidence: a short exact quote from the policy, or "No relevant evidence identified in the uploaded policy."
- explanation: 1-2 sentences explaining your assessment
- risk: "Low" / "Moderate" / "High"
- recommendation: a short actionable suggestion, or "No immediate action needed." if Addressed

Rules:
- Do NOT invent evidence. Only quote text that actually appears in the policy.
- Do NOT claim the organisation is legally compliant or non-compliant.
- Use cautious, academic language.
- Return ONLY the JSON object, no markdown fences, no extra text."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    raw = response.text.strip()
    # Strip markdown code fences if the model adds them
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# ── Demo analysis (keyword-based) ────────────────────────────────────────────
KEYWORDS = {
    "R01": ["notice", "inform", "notification", "disclose"],
    "R02": ["purpose", "reason", "intend", "use your data", "why we collect"],
    "R03": ["personal data", "information we collect", "data we collect", "categories"],
    "R04": ["consent", "agree", "opt-in", "withdraw", "revoke"],
    "R05": ["right", "access", "correction", "erasure", "delete", "nominate"],
    "R06": ["retain", "retention", "storage period", "delete", "erasure", "how long"],
    "R07": ["security", "encrypt", "safeguard", "protect", "ssl", "tls"],
    "R08": ["third party", "third-party", "share", "disclose", "partner", "vendor"],
    "R09": ["grievance", "complaint", "contact us", "reach us", "redressal", "support"],
    "R10": ["child", "children", "minor", "parental consent", "under 18"],
}

def demo_analysis(policy_text, req):
    text_lower = policy_text.lower()
    matched = [kw for kw in KEYWORDS.get(req["id"], []) if kw in text_lower]
    n = len(matched)
    if n >= 2:
        return {
            "status": "Addressed",
            "evidence": f"[DEMO] Relevant keywords found: {', '.join(matched[:3])}",
            "explanation": "Demo Mode: The policy contains relevant language for this requirement (keyword match).",
            "risk": "Low",
            "recommendation": "No immediate action needed based on demo keyword scan.",
        }
    elif n == 1:
        return {
            "status": "Partially Addressed",
            "evidence": f"[DEMO] Partial keyword match: {', '.join(matched)}",
            "explanation": "Demo Mode: Only partial coverage detected. A full AI analysis may reveal more.",
            "risk": "Moderate",
            "recommendation": "Consider adding more explicit language to fully address this requirement.",
        }
    else:
        return {
            "status": "Potential Gap",
            "evidence": "No relevant evidence identified in the uploaded policy.",
            "explanation": "Demo Mode: No relevant keywords found. This may indicate a gap.",
            "risk": "High",
            "recommendation": "Add a dedicated section to address this requirement explicitly.",
        }

def analyse_requirement(policy_text, req, use_ai):
    if use_ai:
        try:
            return analyse_with_gemini(policy_text, req)
        except Exception as e:
            st.warning(f"AI call failed for {req['id']} — using demo fallback. ({e})")
            return demo_analysis(policy_text, req)
    return demo_analysis(policy_text, req)

# ── Score ─────────────────────────────────────────────────────────────────────
def calculate_score(results):
    if not results:
        return 0
    return round(sum(SCORING.get(r["status"], 0) for r in results) / len(results), 1)

# ── HTML report ───────────────────────────────────────────────────────────────
def generate_html_report(requirements, results, score, filename, is_demo):
    now   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    mode  = "Demo Mode (keyword-based)" if is_demo else "AI-Assisted (Google Gemini)"
    rows  = ""
    for req, res in zip(requirements, results):
        st_label = STATUS_EMOJI.get(res.get("status", ""), res.get("status", ""))
        rows += f"""
        <tr>
          <td>{req['id']}</td>
          <td>{req['title']}</td>
          <td>{req['category']}</td>
          <td>{st_label}</td>
          <td style="font-size:11px;">{res.get('evidence','')}</td>
          <td>{res.get('risk','')}</td>
          <td style="font-size:11px;">{res.get('recommendation','')}</td>
        </tr>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DPDP Lens – Assessment Report</title>
<style>
  body{{font-family:'Segoe UI',Arial,sans-serif;margin:48px;color:#1c1c2e;font-size:13px;line-height:1.6;}}
  h1{{font-size:22px;color:#1c1c2e;margin-bottom:4px;}}
  h2{{font-size:15px;color:#1c3557;border-bottom:2px solid #1c3557;padding-bottom:4px;margin-top:32px;}}
  .meta{{color:#555;font-size:12px;margin-bottom:24px;}}
  .disclaimer{{background:#fff8e1;border-left:4px solid #f9a825;padding:10px 16px;
               border-radius:3px;font-size:12px;color:#5d4037;margin-bottom:20px;}}
  .score-box{{display:inline-block;border:2px solid #1c3557;border-radius:4px;
              padding:12px 24px;margin-bottom:24px;}}
  .score-num{{font-size:28px;font-weight:700;color:#1c3557;}}
  .score-note{{font-size:11px;color:#666;margin-top:4px;}}
  table{{border-collapse:collapse;width:100%;margin-top:12px;}}
  th{{background:#1c3557;color:#fff;padding:8px 12px;text-align:left;font-size:12px;font-weight:600;}}
  td{{border:1px solid #ddd;padding:8px 12px;vertical-align:top;}}
  tr:nth-child(even){{background:#f8f9fa;}}
  .footer{{margin-top:40px;font-size:10px;color:#999;border-top:1px solid #ddd;padding-top:12px;}}
</style>
</head>
<body>
<h1>DPDP Lens – Preliminary Policy Assessment Report</h1>
<div class="meta">
  File: <strong>{filename}</strong> &nbsp;|&nbsp;
  Date: <strong>{now}</strong> &nbsp;|&nbsp;
  Mode: <strong>{mode}</strong>
</div>
<div class="disclaimer">&#9888;&#65039; <strong>{DISCLAIMER}</strong></div>
<h2>Preliminary Readiness Score</h2>
<div class="score-box">
  <div class="score-num">{score} <span style="font-size:16px;color:#666;">/ 100</span></div>
  <div class="score-note">
    Policy coverage across {len(requirements)} selected DPDP requirements.<br>
    This is <em>not</em> a legal compliance score.
  </div>
</div>
<h2>Requirement Assessment Results</h2>
<table>
  <tr>
    <th>ID</th><th>Requirement</th><th>Category</th><th>Status</th>
    <th>Policy Evidence</th><th>Risk</th><th>Recommendation</th>
  </tr>
  {rows}
</table>
<div class="footer">
  Generated by DPDP Lens – Academic Prototype &nbsp;|&nbsp; {DISCLAIMER}
</div>
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# UI – CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
}

/* ── Remove default Streamlit top padding ── */
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── App header ── */
.app-header {
    border-bottom: 2px solid #1c3557;
    padding-bottom: 18px;
    margin-bottom: 24px;
}
.app-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 2px 0;
    letter-spacing: -0.5px;
}
.app-header .sub {
    font-size: 0.92rem;
    color: #456;
    margin: 0;
}
.app-header .desc {
    font-size: 0.82rem;
    color: #667;
    margin-top: 6px;
}

/* ── Disclaimer banner ── */
.banner-warning {
    background: #fffbf0;
    border: 1px solid #e8c84a;
    border-left: 4px solid #d4a017;
    padding: 9px 16px;
    border-radius: 4px;
    font-size: 0.80rem;
    color: #5a3e00;
    margin-bottom: 20px;
}

/* ── Info banner (demo mode) ── */
.banner-info {
    background: #f0f6ff;
    border: 1px solid #b0ccee;
    border-left: 4px solid #2a6099;
    padding: 9px 16px;
    border-radius: 4px;
    font-size: 0.82rem;
    color: #1a3f66;
    margin-bottom: 16px;
}

/* ── Section label ── */
.section-label {
    font-size: 0.70rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #2a6099;
    margin-bottom: 6px;
}

/* ── Metric cards ── */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e6ea;
    border-radius: 6px;
    padding: 16px 18px;
    text-align: center;
}
.metric-card .num {
    font-size: 1.85rem;
    font-weight: 700;
    color: #1c1c2e;
    line-height: 1.1;
}
.metric-card .lbl {
    font-size: 0.75rem;
    color: #667;
    margin-top: 4px;
}
.metric-card.green .num { color: #1e6b3b; }
.metric-card.amber  .num { color: #8a5a00; }
.metric-card.red    .num { color: #b01c2e; }

/* ── Score panel ── */
.score-panel {
    background: #f0f4f9;
    border: 1px solid #c8d8ea;
    border-radius: 6px;
    padding: 22px 24px;
    text-align: center;
}
.score-panel .score-num {
    font-size: 2.6rem;
    font-weight: 700;
    color: #1c3557;
    line-height: 1.1;
}
.score-panel .score-denom {
    font-size: 1.1rem;
    color: #8899aa;
    font-weight: 400;
}
.score-panel .score-note {
    font-size: 0.74rem;
    color: #556;
    margin-top: 8px;
    line-height: 1.4;
}

/* ── Status badge ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-addressed   { background: #e6f4ec; color: #1a6b3b; border: 1px solid #a7d7b6; }
.badge-partial     { background: #fff8e6; color: #7a4f00; border: 1px solid #f0c050; }
.badge-gap         { background: #fdf0f0; color: #9b1c1c; border: 1px solid #f5a5a5; }

/* ── Risk badge ── */
.risk-low      { color: #1a6b3b; font-weight: 600; }
.risk-moderate { color: #7a4f00; font-weight: 600; }
.risk-high     { color: #9b1c1c; font-weight: 600; }

/* ── Evidence box ── */
.evidence-box {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-left: 3px solid #6c8ebf;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #333;
    font-style: italic;
    line-height: 1.5;
}

/* ── Field label ── */
.field-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #889;
    margin-bottom: 4px;
}

/* ── Expander header tweaks ── */
summary {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #e2e6ea; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UI – HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
  <h1>⚖️ DPDP Lens</h1>
  <p class="sub">AI-Assisted Privacy Policy Compliance Assessment</p>
  <p class="desc">
    Upload a privacy policy PDF to receive a preliminary assessment against
    selected requirements from the Digital Personal Data Protection (DPDP) Act 2023
    and DPDP Rules 2025.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="banner-warning">
  ⚠️ <strong>{DISCLAIMER}</strong>
</div>
""", unsafe_allow_html=True)

# ── Load requirements ─────────────────────────────────────────────────────────
requirements = load_requirements()

# ── Mode detection ────────────────────────────────────────────────────────────
api_key = get_api_key()
use_ai  = bool(api_key)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 – PDF UPLOAD
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<p class="section-label">Step 1 — Upload Policy PDF</p>', unsafe_allow_html=True)
st.subheader("Upload Privacy Policy")

uploaded_file = st.file_uploader(
    "Select a PDF file to assess",
    type=["pdf"],
    help="Upload the privacy policy document you want to assess against DPDP requirements.",
    label_visibility="collapsed",
)

policy_text = ""
num_pages   = 0

if uploaded_file:
    with st.spinner("Extracting text from PDF…"):
        policy_text, num_pages, error = extract_text_from_pdf(uploaded_file)

    if error:
        st.error(f"❌ {error}")
        policy_text = ""
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="num" style="font-size:1rem;">{uploaded_file.name}</div>
              <div class="lbl">File Name</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
              <div class="num">{num_pages}</div>
              <div class="lbl">Pages Detected</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
              <div class="num">{len(policy_text):,}</div>
              <div class="lbl">Characters Extracted</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if len(policy_text.strip()) < 100:
            st.warning("Very little text extracted. The PDF may be image-based (scanned). Results may not be meaningful.")
        else:
            st.success(f"Text extracted successfully — {len(policy_text):,} characters across {num_pages} page(s).")

        with st.expander("View extracted text (first 2,000 characters)"):
            st.code(policy_text[:2000] + (" …[truncated]" if len(policy_text) > 2000 else ""),
                    language=None)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 – ANALYSE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown('<p class="section-label">Step 2 — Run Assessment</p>', unsafe_allow_html=True)
st.subheader("Analyse Policy")

if not policy_text.strip():
    st.info("Upload a PDF above, then click the button to begin analysis.")

if "results" not in st.session_state:
    st.session_state.results = None
if "analysis_file" not in st.session_state:
    st.session_state.analysis_file = None

analyse_btn = st.button(
    "▶  Analyse Policy",
    disabled=not bool(policy_text.strip()),
    type="primary",
    use_container_width=False,
)

if analyse_btn and policy_text.strip():
    st.session_state.results = []
    st.session_state.analysis_file = uploaded_file.name if uploaded_file else "unknown.pdf"
    n_req = len(requirements)
    bar   = st.progress(0, text="Preparing…")

    for i, req in enumerate(requirements):
        bar.progress((i + 1) / n_req,
                     text=f"Assessing [{req['id']}] {req['title']}  ({i+1}/{n_req})")
        result = analyse_requirement(policy_text, req, use_ai)
        result.update({k: req[k] for k in ("id", "title", "category",
                                            "legal_source", "assessment_question")})
        st.session_state.results.append(result)

    bar.empty()
    st.success("Assessment complete. Results are shown below.")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 – RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.results:
    results = st.session_state.results
    score   = calculate_score(results)

    counts = {"Addressed": 0, "Partially Addressed": 0, "Potential Gap": 0}
    for r in results:
        counts[r.get("status", "Potential Gap")] += 1

    # ── Summary ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-label">Step 3 — Summary</p>', unsafe_allow_html=True)
    st.subheader("Assessment Summary")

    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown(f"""
        <div class="score-panel">
          <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;
               letter-spacing:0.08em;color:#6688aa;margin-bottom:8px;">
            Preliminary Readiness Score
          </div>
          <div class="score-num">
            {score}<span class="score-denom"> / 100</span>
          </div>
          <div class="score-note">
            Coverage across {len(requirements)} selected DPDP requirements.<br>
            This is <strong>not</strong> a legal compliance score.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="num">{len(requirements)}</div>
              <div class="lbl">Requirements Assessed</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class="metric-card green">
              <div class="num">{counts['Addressed']}</div>
              <div class="lbl">Addressed</div>
            </div>""", unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="metric-card amber">
              <div class="num">{counts['Partially Addressed']}</div>
              <div class="lbl">Partially Addressed</div>
            </div>""", unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div class="metric-card red">
              <div class="num">{counts['Potential Gap']}</div>
              <div class="lbl">Potential Gaps</div>
            </div>""", unsafe_allow_html=True)

    # Simple bar chart
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col, _ = st.columns([2, 1])
    with chart_col:
        import pandas as pd
        chart_df = pd.DataFrame({
            "Status": ["Addressed", "Partially Addressed", "Potential Gap"],
            "Count":  [counts["Addressed"], counts["Partially Addressed"], counts["Potential Gap"]],
        })
        st.bar_chart(chart_df.set_index("Status"), use_container_width=True, height=200)

    st.caption(
        "Scoring method: Addressed = 100 pts | Partially Addressed = 50 pts | "
        "Potential Gap = 0 pts.  Score = simple average across all assessed requirements."
    )
    if not use_ai:
        st.caption("⚠️ Demo Mode: results are based on keyword matching, not AI analysis.")

    # ── Detailed results ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-label">Step 4 — Detailed Results</p>', unsafe_allow_html=True)
    st.subheader("Requirement-Level Assessment")
    st.caption(
        "Each section below shows the assessment for one DPDP requirement. "
        "Click to expand. All assessments are preliminary."
    )

    for result in results:
        status = result.get("status", "Potential Gap")
        risk   = result.get("risk", RISK_MAP.get(status, ""))

        # Expander label
        if status == "Addressed":
            badge_cls = "badge-addressed"; prefix = "✅"
        elif status == "Partially Addressed":
            badge_cls = "badge-partial";   prefix = "⚠️"
        else:
            badge_cls = "badge-gap";       prefix = "🔴"

        risk_cls = {"Low": "risk-low", "Moderate": "risk-moderate",
                    "High": "risk-high"}.get(risk, "")

        with st.expander(
            f"{prefix}  [{result['id']}]  {result['title']}  —  {result['category']}",
            expanded=False,
        ):
            top_l, top_r = st.columns([3, 1])

            with top_l:
                st.markdown(
                    f'<p class="field-label">Requirement</p>'
                    f'<p style="margin:0 0 12px 0;">{result["title"]}</p>'
                    f'<p class="field-label">Category</p>'
                    f'<p style="margin:0 0 12px 0;">{result["category"]}</p>'
                    f'<p class="field-label">Legal Reference</p>'
                    f'<p style="margin:0 0 12px 0;">{result["legal_source"]}</p>'
                    f'<p class="field-label">Assessment Question</p>'
                    f'<p style="margin:0;font-style:italic;">{result["assessment_question"]}</p>',
                    unsafe_allow_html=True,
                )

            with top_r:
                st.markdown(
                    f'<p class="field-label">Status</p>'
                    f'<span class="badge {badge_cls}">{STATUS_EMOJI.get(status, status)}</span>'
                    f'<br><br>'
                    f'<p class="field-label">Risk Level</p>'
                    f'<span class="{risk_cls}">{risk}</span>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            evidence = result.get("evidence") or "No relevant evidence identified in the uploaded policy."
            st.markdown(
                f'<p class="field-label">Policy Evidence</p>'
                f'<div class="evidence-box">{evidence}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<br><p class="field-label">Explanation</p>'
                f'<p style="font-size:0.88rem;margin:0 0 12px 0;">'
                f'{result.get("explanation","")}</p>',
                unsafe_allow_html=True,
            )

            rec = result.get("recommendation", "")
            if rec:
                st.markdown(
                    f'<p class="field-label">Recommendation</p>'
                    f'<p style="font-size:0.88rem;margin:0;">{rec}</p>',
                    unsafe_allow_html=True,
                )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-label">Step 5 — Export</p>', unsafe_allow_html=True)
    st.subheader("Download Assessment Report")

    report_html = generate_html_report(
        requirements, results, score,
        st.session_state.analysis_file,
        is_demo=not use_ai,
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    st.download_button(
        label="⬇  Download HTML Report",
        data=report_html.encode("utf-8"),
        file_name=f"dpdp_lens_report_{timestamp}.html",
        mime="text/html",
        use_container_width=False,
    )
    st.caption(
        "The report is a self-contained HTML file. Open it in any web browser. "
        f"{DISCLAIMER}"
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f'<p style="text-align:center;font-size:0.75rem;color:#889;">'
    f'DPDP Lens — Academic Prototype &nbsp;·&nbsp; {DISCLAIMER}'
    f'</p>',
    unsafe_allow_html=True,
)
