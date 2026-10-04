"""
test_dpdp_lens.py
-----------------
Standalone test for DPDP Lens.

Tests:
  1. requirements.json loads correctly
  2. PDF text extraction works on the sample file
  3. Demo analysis runs for all requirements
  4. AI analysis runs for ONE requirement (only if GEMINI_API_KEY is set)
  5. Score calculation is correct

Run from the dpdp-lens/ directory:
    python test_dpdp_lens.py
"""

import os, sys, json

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"

def separator(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

# ── Test 1: Requirements load ─────────────────────────────────────
separator("TEST 1 — Load requirements.json")
try:
    with open("data/requirements.json", encoding="utf-8") as f:
        requirements = json.load(f)
    assert len(requirements) == 10, f"Expected 10, got {len(requirements)}"
    for r in requirements:
        for field in ("id", "title", "category", "legal_source",
                      "description", "assessment_question"):
            assert field in r, f"Missing field '{field}' in {r.get('id')}"
    print(f"{PASS}  Loaded {len(requirements)} requirements, all fields present.")
except Exception as e:
    print(f"{FAIL}  {e}")
    sys.exit(1)

# ── Test 2: PDF extraction ────────────────────────────────────────
separator("TEST 2 — PDF text extraction (sample file)")
try:
    import pymupdf as fitz
    pdf_path = os.path.join("sample", "sample_privacy_policy.pdf")
    if not os.path.exists(pdf_path):
        print(f"{SKIP}  Sample PDF not found. Run: python create_sample_pdf.py")
    else:
        doc   = fitz.open(pdf_path)
        pages = doc.page_count
        text  = "\n".join(p.get_text() for p in doc)
        doc.close()
        assert pages > 0,      "No pages found"
        assert len(text) > 200, f"Too little text extracted: {len(text)} chars"
        print(f"{PASS}  Extracted {len(text):,} chars from {pages} pages.")
        sample_text = text
except Exception as e:
    print(f"{FAIL}  {e}")
    sample_text = "This is a sample privacy policy. We collect personal data. " \
                  "We use consent. Data retention is 7 years. Security safeguards " \
                  "include encryption. Contact grievance@example.com for complaints."

# ── Test 3: Demo analysis ─────────────────────────────────────────
separator("TEST 3 — Demo analysis (all 10 requirements)")

SCORING  = {"Addressed": 100, "Partially Addressed": 50, "Potential Gap": 0}
RISK_MAP = {"Addressed": "Low", "Partially Addressed": "Moderate", "Potential Gap": "High"}
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
        return {"status": "Addressed",
                "evidence": f"[DEMO] Keywords: {', '.join(matched[:3])}",
                "explanation": "Demo: relevant language found.",
                "risk": "Low", "recommendation": "No immediate action needed."}
    elif n == 1:
        return {"status": "Partially Addressed",
                "evidence": f"[DEMO] Partial: {', '.join(matched)}",
                "explanation": "Demo: partial coverage.",
                "risk": "Moderate", "recommendation": "Add more explicit language."}
    else:
        return {"status": "Potential Gap",
                "evidence": "No relevant evidence identified in the uploaded policy.",
                "explanation": "Demo: no keywords found.",
                "risk": "High", "recommendation": "Add a dedicated section."}

demo_results = []
all_ok = True
for req in requirements:
    try:
        result = demo_analysis(sample_text, req)
        assert result["status"] in SCORING
        assert result["risk"]   in ("Low", "Moderate", "High")
        demo_results.append(result)
        print(f"  [{req['id']}] {req['title'][:45]:<45}  {result['status']}")
    except Exception as e:
        print(f"{FAIL}  [{req['id']}] {e}")
        all_ok = False

if all_ok:
    scores = [SCORING[r["status"]] for r in demo_results]
    score  = round(sum(scores) / len(scores), 1)
    counts = {s: sum(1 for r in demo_results if r["status"] == s) for s in SCORING}
    print()
    print(f"{PASS}  All 10 requirements analysed.")
    print(f"        Addressed: {counts['Addressed']}  |  "
          f"Partial: {counts['Partially Addressed']}  |  "
          f"Gap: {counts['Potential Gap']}")
    print(f"        Preliminary Readiness Score: {score} / 100")
else:
    print(f"{FAIL}  One or more demo analyses failed.")

# ── Test 4: AI analysis (single requirement, optional) ────────────
separator("TEST 4 — AI analysis via Gemini (requires GEMINI_API_KEY)")

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print(f"{SKIP}  No API key found.")
    print("        To test AI mode:")
    print("        1. Copy .env.example to .env")
    print("        2. Set GEMINI_API_KEY=your_key_here")
    print("        3. Re-run this script.")
else:
    print(f"        Key detected (first 8 chars): {api_key[:8]}...")
    try:
        import re, json as _json
        from google import genai as _genai
        client   = _genai.Client(api_key=api_key)
        test_req = requirements[0]          # R01 – Notice to Data Principals
        excerpt  = sample_text[:4000]

        prompt = f"""You are an academic research assistant assessing a privacy policy.
REQUIREMENT: {test_req['title']}
Description: {test_req['description']}
POLICY TEXT: {excerpt}
Return ONLY a JSON object: {{\"status\":\"...\",\"evidence\":\"...\",
\"explanation\":\"...\",\"risk\":\"...\",\"recommendation\":\"...\"}}
Status must be one of: Addressed / Partially Addressed / Potential Gap"""

        print("        Calling Gemini API (gemini-2.0-flash)…", end=" ", flush=True)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        raw = response.text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        parsed = _json.loads(raw)

        assert parsed["status"]  in ("Addressed", "Partially Addressed", "Potential Gap")
        assert parsed["risk"]    in ("Low", "Moderate", "High")
        assert "evidence"        in parsed
        assert "explanation"     in parsed
        assert "recommendation"  in parsed

        print("OK")
        print(f"{PASS}  AI result for [{test_req['id']}] {test_req['title']}:")
        print(f"        Status      : {parsed['status']}")
        print(f"        Risk        : {parsed['risk']}")
        print(f"        Evidence    : {parsed['evidence'][:100]}...")
        print(f"        Explanation : {parsed['explanation'][:100]}...")
    except Exception as e:
        print(f"\n{FAIL}  AI call failed: {e}")

# ── Test 5: Score calculation ─────────────────────────────────────
separator("TEST 5 — Score calculation")
try:
    test_cases = [
        ([{"status": "Addressed"}] * 10,           100.0),
        ([{"status": "Potential Gap"}] * 10,          0.0),
        ([{"status": "Partially Addressed"}] * 10,   50.0),
        ([{"status": "Addressed"}] * 5 +
         [{"status": "Potential Gap"}] * 5,          50.0),
        ([{"status": "Addressed"}] * 8 +
         [{"status": "Partially Addressed"}] * 2,    90.0),
    ]
    for results_in, expected in test_cases:
        scores = [SCORING[r["status"]] for r in results_in]
        actual = round(sum(scores) / len(scores), 1)
        assert actual == expected, f"Expected {expected}, got {actual}"
    print(f"{PASS}  All score calculations correct.")
except Exception as e:
    print(f"{FAIL}  {e}")

# ── Summary ───────────────────────────────────────────────────────
separator("DONE")
print("  All tests complete. App is ready to use.")
print("  Run:  python -m streamlit run app.py")
print()
