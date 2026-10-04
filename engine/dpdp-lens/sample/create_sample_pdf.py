"""
Generates a synthetic sample privacy policy PDF for DPDP Lens demonstration.

The policy is intentionally designed to show mixed results:
  - CLEARLY ADDRESSED:    Notice, Security, Grievance
  - PARTIALLY ADDRESSED:  Purpose, Consent, Data Sharing, Retention
  - POTENTIAL GAPS:       Right to Erasure, Right to Access/Correction

Run once: python sample/create_sample_pdf.py
"""

import pymupdf as fitz
import os

# ---------------------------------------------------------------------------
# Full text of the synthetic privacy policy
# ---------------------------------------------------------------------------
PAGES = [

# PAGE 1
"""SYNTHETIC DEMONSTRATION DOCUMENT — FOR ACADEMIC USE ONLY
================================================================
PRIVACY POLICY
DataCorp Technologies Private Limited
================================================================
Effective Date: 01 January 2024  |  Version: 1.0

IMPORTANT: This is a synthetic document created solely to demonstrate
the DPDP Lens academic prototype. It does not represent any real
organisation or real data practices.
================================================================

NOTICE TO DATA PRINCIPALS
--------------------------
DataCorp Technologies Private Limited ("DataCorp", "we", "our") is
committed to protecting your personal data. Before you use our
products or services, we want you to understand what personal data
we collect, why we collect it, how we use it, and what rights you
have in relation to it.

Please read this Privacy Policy carefully. By registering for or
using our services, you acknowledge that you have read and understood
this Privacy Policy.


CATEGORIES OF PERSONAL DATA COLLECTED
--------------------------------------
We collect the following categories of personal data from you:

  1. Identity Data
     - Full name
     - Date of birth
     - Gender

  2. Contact Data
     - Email address
     - Mobile phone number
     - Postal / billing address

  3. Account & Credentials Data
     - Username
     - Password (stored in encrypted, hashed form only)
     - Account preferences and settings

  4. Usage and Technical Data
     - Pages visited and features used
     - Time and duration of sessions
     - IP address, browser type, operating system
     - Device identifiers and cookies

  5. Transaction Data
     - Order history and purchase records
     - Payment method type (we never store full card numbers)

We do NOT intentionally collect sensitive personal data such as
biometric data, health records, or government identity numbers
unless a specific service requires it and you have given explicit
consent for that purpose.
""",

# PAGE 2
"""================================================================
PURPOSE OF PROCESSING PERSONAL DATA
-------------------------------------
We use your personal data for general operational purposes including
improving our services, managing your account, communicating with
you, and complying with legal obligations. We may also use your data
for analytics, marketing, and other business activities as they arise.


CONSENT
--------
When you register for DataCorp services, you agree to this Privacy
Policy. By continuing to use our services, you consent to the
collection and use of your data as described here.

If you no longer wish to use our services, you may deactivate your
account by contacting our support team.

Note: We rely on your consent as a legal basis for processing where
required. The specific process for withdrawing consent for individual
processing activities is not detailed in this version of the policy
and will be updated in a future revision.


DATA RETENTION
---------------
We retain your personal data for as long as it is necessary for our
business operations and to comply with our legal obligations. Data
may be retained for extended periods if required for ongoing legal
proceedings or regulatory requirements.

We periodically review the data we hold. If data is found to be
outdated or no longer required, it may be deleted or anonymised,
subject to our internal review processes.

Note: This policy does not currently specify fixed retention periods
for each category of data. Specific retention schedules will be
defined in a future policy update.


SECURITY SAFEGUARDS
---------------------
We implement industry-standard technical and organisational security
measures to protect your personal data from unauthorised access,
disclosure, alteration, or destruction. These measures include:

  - AES-256 encryption for all data stored at rest
  - TLS 1.3 encryption for all data transmitted over the network
  - Role-based access controls (RBAC) to restrict data access
    to authorised personnel only
  - Multi-factor authentication (MFA) for all administrative access
  - Regular vulnerability assessments and penetration testing
  - Automated intrusion detection systems
  - Documented incident response and breach notification procedures

In the event of a personal data breach that poses a risk to your
rights, we will notify you and the relevant regulatory authority
without undue delay.
""",

# PAGE 3
"""================================================================
DATA SHARING AND THIRD-PARTY DISCLOSURE
-----------------------------------------
We may share your personal data with third parties in the following
circumstances:

  1. Service Providers: We work with trusted third-party vendors
     and partners who assist us in delivering our platform (for
     example, cloud hosting, payment processing, email services,
     analytics). These parties are permitted to process your data
     only as directed by us and are bound by confidentiality
     obligations.

  2. Legal Requirements: We may disclose your personal data to
     law enforcement agencies, courts, or other government bodies
     when required by applicable law or a valid legal order.

  3. Business Transfers: In the event of a merger, acquisition,
     restructuring, or sale of assets, your personal data may be
     transferred as part of that transaction.

We do not sell your personal data to third parties for their own
marketing or commercial purposes.

Note: This policy does not currently provide a specific list of
named third-party recipients or the categories of recipients.


GRIEVANCE REDRESSAL MECHANISM
-------------------------------
DataCorp takes all privacy concerns and complaints seriously. If you
have any questions, concerns, or complaints about this Privacy Policy
or the manner in which your personal data is handled, please contact
our Data Protection Officer:

  Data Protection Officer
  DataCorp Technologies Private Limited
  Email:   dpo@datacorp.in
  Phone:   +91-11-4567-8900
  Address: 5th Floor, Tech Tower, Sector 44,
           Gurugram, Haryana 122003, India

Upon receiving your complaint or query, we will:
  - Acknowledge receipt within 3 (three) business days
  - Investigate the matter in a fair and objective manner
  - Provide you with a substantive written response within 30 days

If you are not satisfied with the resolution provided by our DPO,
you may escalate your complaint to the Data Protection Board of
India, once constituted under the DPDP Act, 2023.


================================================================
DISCLAIMER
================================================================
This Privacy Policy is a synthetic demonstration document created
for academic and educational purposes only as part of the DPDP Lens
prototype project. It does not represent any real organisation,
real data practices, or real legal obligations.

================================================================
END OF SYNTHETIC PRIVACY POLICY DOCUMENT
================================================================
"""
]


def create_sample_pdf():
    output_path = os.path.join(os.path.dirname(__file__), "sample_privacy_policy.pdf")
    doc = fitz.open()

    for page_text in PAGES:
        page = doc.new_page(width=595, height=842)   # A4
        rect = fitz.Rect(50, 60, 545, 810)
        page.insert_textbox(
            rect,
            page_text,
            fontsize=9,
            fontname="Courier",
            color=(0, 0, 0),
            align=0,
        )

    doc.save(output_path)
    doc.close()
    print(f"Sample PDF created at: {output_path}")
    print(f"Pages: {len(PAGES)}")


if __name__ == "__main__":
    create_sample_pdf()
