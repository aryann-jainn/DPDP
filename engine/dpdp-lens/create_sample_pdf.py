"""
create_sample_pdf.py
--------------------
Creates sample/sample_privacy_policy.pdf – a synthetic demonstration document
for testing DPDP Lens. Run once before demonstrating the application.

Usage:  python create_sample_pdf.py
"""

import os
import sys

# ── Policy text ───────────────────────────────────────────────────────────────
POLICY_TEXT = """\
================================================================
SYNTHETIC DEMONSTRATION DOCUMENT – NOT A REAL PRIVACY POLICY
Created for academic testing of DPDP Lens (MCLIS Project)
================================================================

PRIVACY POLICY
DataSeva Technologies Private Limited

Effective Date: 1 October 2024

----------------------------------------------------------------
ABOUT THIS DOCUMENT
----------------------------------------------------------------

This is a synthetic privacy policy created solely to demonstrate the
DPDP Lens academic prototype. It is intentionally designed so that
some requirements under the Digital Personal Data Protection Act 2023
are clearly addressed, some are only partially addressed, and some are
absent altogether, enabling a meaningful demonstration of the tool.

----------------------------------------------------------------
PAGE 1 – INTRODUCTION AND NOTICE TO DATA PRINCIPALS
----------------------------------------------------------------

1.  INTRODUCTION

    DataSeva Technologies Private Limited ("DataSeva", "we", "our",
    "the Company") operates an online platform providing document
    management and e-signature services to individuals and businesses
    across India.

    We are committed to handling your personal data responsibly. This
    Privacy Policy is provided to all Data Principals as a formal
    notice in accordance with applicable law. It describes:

    - What personal data we collect and why.
    - How we use, store, and share that data.
    - What rights you have and how to exercise them.
    - How to contact us with concerns or complaints.

    Please read this policy carefully before using our services.

2.  PERSONAL DATA WE COLLECT

    We collect the following categories of personal data from our users:

    (a) Identity information: Full name, date of birth, government-issued
        identification number (Aadhaar, PAN), photograph.

    (b) Contact information: Email address, mobile number, mailing address.

    (c) Account information: Username, encrypted password, account
        preferences and settings.

    (d) Document data: Files, forms, and attachments uploaded to our
        platform. These may contain personal data of third parties.

    (e) Payment information: Bank account details or UPI handles, which
        are processed through PCI-DSS compliant payment gateways.

    (f) Usage data: IP address, browser type, operating system, pages
        visited, session duration, and clickstream data.

    (g) Device data: Device identifiers, mobile device model, and
        operating system version.

    We do not collect special category data (biometric, health, or
    caste-related data) unless expressly required by a specific service
    and disclosed separately.

----------------------------------------------------------------
PAGE 2 – PURPOSE OF PROCESSING AND CONSENT
----------------------------------------------------------------

3.  PURPOSES OF PROCESSING PERSONAL DATA

    We collect and process personal data strictly for the following
    specified purposes:

    (a) Account management: To create, verify, and maintain your
        user account.

    (b) Service delivery: To provide document management, e-signature,
        and collaboration features.

    (c) Billing: To process payments and issue invoices.

    (d) Customer support: To respond to queries, complaints, and
        service requests.

    (e) Regulatory compliance: To meet legal and statutory obligations,
        including responding to lawful government requests.

    (f) Service improvement: To analyse usage patterns and improve
        platform functionality.

    We do not process your personal data for direct marketing or
    profiling purposes without your separate, explicit consent.
    We do not sell personal data to third parties under any circumstances.

4.  CONSENT

    By registering for and using our services, you provide your free,
    specific, informed, unconditional, and unambiguous consent to the
    processing of your personal data as described in this policy.

    You may withdraw your consent at any time by:

    - Sending a written request to privacy@dataseva.in, or
    - Using the "Withdraw Consent" option in your account settings.

    Upon receipt of a valid withdrawal request, we will cease processing
    your personal data for non-essential purposes within 15 working days,
    except where retention is required by law. Withdrawal of consent
    does not affect the lawfulness of processing that occurred before
    the withdrawal.

    Note: Withdrawal of consent for essential processing may affect your
    ability to continue using certain services.

----------------------------------------------------------------
PAGE 3 – YOUR RIGHTS AND DATA RETENTION
----------------------------------------------------------------

5.  YOUR RIGHTS AS A DATA PRINCIPAL

    Under the Digital Personal Data Protection Act 2023, you have the
    right to:

    (a) Right to Access: Request a summary of the personal data we hold
        about you and information about how it has been processed.

    (b) Right to Correction and Erasure: Request correction of inaccurate
        or incomplete personal data. You may also request erasure of your
        data where it is no longer necessary for the stated purpose.

    (c) Right to Grievance Redressal: If you believe your rights have
        been violated, you may lodge a complaint with our Grievance
        Officer (see Section 9) or approach the Data Protection Board
        of India.

    (d) Right to Nominate: You may nominate another individual to exercise
        your rights under this Act in the event of your death or
        incapacity.

    To exercise any of the above rights, please submit a request to
    privacy@dataseva.in. We will respond within 30 days of receipt.

6.  DATA RETENTION

    We retain your personal data only as long as necessary for the
    purpose for which it was collected or as required by law.

    Indicative retention periods:
    - Account data: Retained for the duration of your account, plus
      1 year after account closure.
    - Transaction records: 7 years, as required under financial
      regulations.
    - Customer support records: 2 years from date of resolution.
    - Usage logs: 90 days on a rolling basis.

    Upon expiry of the applicable retention period, personal data is
    securely erased or de-identified such that it can no longer be
    attributed to an identified individual.

    [NOTE – Partial Coverage: We acknowledge that specific criteria
    for deletion upon withdrawal of consent are not fully articulated
    in this version of the policy and will be updated.]

----------------------------------------------------------------
PAGE 4 – SECURITY, DATA SHARING, AND GRIEVANCE
----------------------------------------------------------------

7.  SECURITY SAFEGUARDS

    DataSeva implements appropriate technical and organisational
    security measures to protect personal data from unauthorised
    access, loss, destruction, or disclosure. These measures include:

    - TLS/SSL encryption for data in transit.
    - AES-256 encryption for data at rest.
    - Role-based access controls restricting data access to authorised
      personnel only.
    - Periodic security assessments and vulnerability scans.
    - Formal incident response procedures.

    In the event of a personal data breach that is likely to result in
    risk to Data Principals, we will notify the Data Protection Board of
    India as required by law, and affected individuals where applicable.

8.  DATA SHARING AND THIRD-PARTY DISCLOSURE

    We do not sell personal data. We may share personal data only in
    the following circumstances:

    (a) Service providers: With third-party vendors who assist in
        operating our platform, such as cloud hosting (AWS/Azure),
        payment processing (Razorpay), and email delivery (SendGrid).
        All such vendors are engaged via valid data processing agreements.

    (b) Legal obligation: With government or regulatory authorities when
        required by law, court order, or lawful directions.

    (c) Business transfers: In the event of a merger, acquisition, or
        sale of assets, personal data may be transferred to the successor
        entity, subject to this policy.

    All third-party Data Processors are contractually obligated to
    process personal data only as instructed, and to implement
    appropriate security safeguards.

9.  GRIEVANCE REDRESSAL

    If you have a complaint, concern, or query regarding the handling
    of your personal data, please contact our Grievance Officer:

    Name:        Mr. Arvind Kulkarni
    Designation: Grievance Officer
    Email:       grievance@dataseva.in
    Phone:       1800-555-7890 (Mon–Fri, 10 AM–6 PM IST)
    Address:     DataSeva Technologies Pvt. Ltd.
                 3rd Floor, InnoSpace, Hinjewadi Phase II,
                 Pune – 411057, Maharashtra, India

    We will acknowledge your complaint within 48 hours and resolve it
    within 30 working days. If you are not satisfied with our resolution,
    you may escalate the matter to the Data Protection Board of India.

----------------------------------------------------------------
PAGE 5 – CHILDREN'S DATA AND MISCELLANEOUS
----------------------------------------------------------------

10. PROCESSING OF CHILDREN'S PERSONAL DATA

    Our platform and services are intended for use by adults only.
    We do not knowingly collect or process personal data of children
    under the age of 18.

    Our registration process requires users to confirm that they are
    18 years of age or older.

    [NOTE – Gap Identified for Demo: This policy does not describe the
    process for verifiable parental/guardian consent in cases where
    children's data is inadvertently collected, as required under
    Section 9 of the DPDP Act 2023. This is an intentional gap
    for demonstration purposes.]

11. UPDATES TO THIS POLICY

    We may update this Privacy Policy from time to time to reflect
    changes in our practices, services, or applicable law. Material
    changes will be communicated through a prominent notice on our
    website or via email, with adequate prior notice. Continued use
    of our services after the effective date of the updated policy
    constitutes acceptance.

12. CONTACT US

    For any questions regarding this Privacy Policy:

    Email:   privacy@dataseva.in
    Website: www.dataseva.in/privacy
    Post:    Data Protection Officer, DataSeva Technologies Pvt. Ltd.,
             3rd Floor, InnoSpace, Hinjewadi Phase II, Pune – 411057.

================================================================
END OF DOCUMENT
SYNTHETIC DEMONSTRATION DATA – CREATED FOR DPDP LENS (ACADEMIC PROTOTYPE)
================================================================
"""


def create_sample_pdf():
    try:
        import pymupdf as fitz
    except ImportError:
        print("[ERROR] PyMuPDF not installed. Run: python -m pip install pymupdf")
        sys.exit(1)

    # ── Page constants ─────────────────────────────────────────────────────────
    PAGE_W = 595   # A4 width in points
    PAGE_H = 842   # A4 height in points
    MARGIN_L = 65
    MARGIN_R = 65
    MARGIN_T = 65
    MARGIN_B = 65
    TEXT_W   = PAGE_W - MARGIN_L - MARGIN_R

    FONT_NORMAL  = "helv"   # built-in Helvetica
    FONT_BOLD    = "hebo"   # built-in Helvetica-Bold
    SIZE_BODY    = 10
    SIZE_HEADING = 11
    SIZE_SMALL   = 8.5
    LEADING      = 5        # extra gap between lines

    COLOR_DARK   = (0.10, 0.10, 0.15)
    COLOR_MID    = (0.30, 0.30, 0.35)
    COLOR_ACCENT = (0.05, 0.27, 0.45)   # dark navy-blue for headings
    COLOR_RULE   = (0.70, 0.70, 0.75)

    doc = fitz.open()

    def new_page():
        p = doc.new_page(width=PAGE_W, height=PAGE_H)
        return p, MARGIN_T

    def draw_rule(page, y, color=COLOR_RULE):
        page.draw_line(
            fitz.Point(MARGIN_L, y),
            fitz.Point(PAGE_W - MARGIN_R, y),
            color=color, width=0.5
        )

    def draw_text_block(page, y, text, font=FONT_NORMAL, size=SIZE_BODY,
                        color=COLOR_DARK, indent=0):
        """
        Word-wrap `text` within TEXT_W - indent, write to page, return new y.
        Returns (new_y, page) – creates a new page if we overflow.
        """
        x = MARGIN_L + indent
        avail_w = TEXT_W - indent
        words = text.split()
        line_buf = ""
        lines_out = []

        for word in words:
            trial = (line_buf + " " + word).strip()
            # estimate width: approx 0.56 * size * nchars for proportional font
            est_w = len(trial) * size * 0.56
            if est_w > avail_w and line_buf:
                lines_out.append(line_buf)
                line_buf = word
            else:
                line_buf = trial
        if line_buf:
            lines_out.append(line_buf)

        for ln in lines_out:
            if y + size + LEADING > PAGE_H - MARGIN_B:
                page, y = new_page()
            page.insert_text(fitz.Point(x, y), ln,
                             fontname=font, fontsize=size, color=color)
            y += size + LEADING

        return page, y

    # ═══════════════════════════════
    # Build pages from POLICY_TEXT
    # ═══════════════════════════════
    page, y = new_page()

    for raw_line in POLICY_TEXT.split("\n"):
        line = raw_line.rstrip()

        # Page break markers
        if line.startswith("---"):
            draw_rule(page, y + 2)
            y += 10
            continue

        if line.startswith("==="):
            draw_rule(page, y + 2, color=COLOR_ACCENT)
            y += 10
            continue

        # Blank line
        if line.strip() == "":
            y += SIZE_BODY
            continue

        # Section headings (ALL CAPS + single short line)
        if line.strip() == line.strip().upper() and len(line.strip()) > 4:
            if y + SIZE_HEADING + LEADING > PAGE_H - MARGIN_B:
                page, y = new_page()
            page.insert_text(
                fitz.Point(MARGIN_L, y),
                line.strip(),
                fontname=FONT_BOLD,
                fontsize=SIZE_HEADING,
                color=COLOR_ACCENT,
            )
            y += SIZE_HEADING + LEADING + 2
            continue

        # Numbered section headings like "1.  INTRODUCTION"
        stripped = line.strip()
        if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ".":
            if y + SIZE_HEADING + LEADING > PAGE_H - MARGIN_B:
                page, y = new_page()
            page.insert_text(
                fitz.Point(MARGIN_L, y),
                stripped,
                fontname=FONT_BOLD,
                fontsize=SIZE_HEADING,
                color=COLOR_ACCENT,
            )
            y += SIZE_HEADING + LEADING + 2
            continue

        # [NOTE] lines – use italic styling (different color)
        if stripped.startswith("[NOTE") or stripped.startswith("[ERROR"):
            page, y = draw_text_block(
                page, y, stripped,
                font=FONT_BOLD, size=SIZE_SMALL, color=(0.55, 0.27, 0.07), indent=8
            )
            y += 2
            continue

        # Sub-items like "(a)", "(b)"
        if stripped.startswith("(") and len(stripped) > 3 and stripped[2] in "):":
            page, y = draw_text_block(
                page, y, stripped,
                font=FONT_NORMAL, size=SIZE_BODY, color=COLOR_DARK, indent=16
            )
            continue

        # Bullet / dash items
        if stripped.startswith("- ") or stripped.startswith("* "):
            page, y = draw_text_block(
                page, y, "•  " + stripped[2:],
                font=FONT_NORMAL, size=SIZE_BODY, color=COLOR_DARK, indent=16
            )
            continue

        # Regular body text (may be indented in source)
        indent = 8 if line.startswith("    ") else 0
        page, y = draw_text_block(
            page, y, stripped,
            font=FONT_NORMAL, size=SIZE_BODY, color=COLOR_DARK, indent=indent
        )

    # ── Footer on every page ──────────────────────────────────────────────────
    for i, pg in enumerate(doc):
        footer_y = PAGE_H - MARGIN_B + 14
        draw_rule(pg, footer_y - 6, color=COLOR_RULE)
        pg.insert_text(
            fitz.Point(MARGIN_L, footer_y),
            "SYNTHETIC DEMONSTRATION DATA — DPDP Lens Academic Prototype",
            fontname=FONT_NORMAL, fontsize=7.5, color=COLOR_MID,
        )
        pg.insert_text(
            fitz.Point(PAGE_W - MARGIN_R - 30, footer_y),
            f"Page {i + 1}",
            fontname=FONT_NORMAL, fontsize=7.5, color=COLOR_MID,
        )

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "sample", "sample_privacy_policy.pdf"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pages = doc.page_count   # read before closing
    doc.save(out_path)
    doc.close()

    print(f"[OK] Sample PDF created  : {out_path}")
    print(f"[OK] Pages               : {pages}")
    print(f"[OK] Size                : {os.path.getsize(out_path):,} bytes")
    print()
    print("Coverage summary (intentional for demo):")
    print("  Clearly Addressed    : Notice, Purpose, Data Types, Consent,")
    print("                         Rights, Retention, Security, Data Sharing,")
    print("                         Grievance")
    print("  Partially Addressed  : Children's Data (age gate only, no parental")
    print("                         consent process described), Retention criteria")
    print("                         on consent withdrawal")
    print("  Potential Gap        : Verifiable parental consent mechanism (Section 9)")


if __name__ == "__main__":
    create_sample_pdf()
