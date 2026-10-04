"""
Comprehensive Audit Report Generator for Port Security Policy Auditor.
Produces publication-grade PDF audit reports via ReportLab,
along with structured Markdown and JSON exports for GRC compliance ingestion.
"""

from typing import Dict, List, Any
import io
import json
import datetime
import hashlib

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)


def generate_pdf_report(
    scenario_name: str,
    device_type: str,
    port_interface: str,
    environment: str,
    user_privilege: str,
    data_classification: str,
    intended_action: str,
    risk_data: Dict[str, Any],
    sanitization_data: Dict[str, Any],
    cisco_commands: str,
    ps_scripts: Dict[str, str],
    compliance_results: List[Dict[str, Any]],
    auditor_name: str = "Chief Information Security Officer (CISO)",
    organization_name: str = "Enterprise Global Security Operations"
) -> bytes:
    """Generates a professional multi-page PDF compliance audit report."""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography & Palette
    primary_color = colors.HexColor("#0f172a") # Dark Slate
    accent_blue = colors.HexColor("#0284c7")   # Sky Blue
    text_dark = colors.HexColor("#1e293b")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")
    
    # Risk Level Color
    risk_level = risk_data["risk_level"]
    if risk_level == "LOW":
        risk_hex = colors.HexColor("#10b981")
    elif risk_level == "MEDIUM":
        risk_hex = colors.HexColor("#f59e0b")
    elif risk_level == "HIGH":
        risk_hex = colors.HexColor("#f97316")
    else:
        risk_hex = colors.HexColor("#ef4444")

    # Document Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=accent_blue,
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )

    code_style = ParagraphStyle(
        'CodeStyleCustom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )
    
    story = []
    
    # 1. Header Banner & Meta
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_id = f"AUD-{hashlib.sha256(f'{scenario_name}{timestamp}'.encode()).hexdigest()[:10].upper()}"
    
    header_data = [
        [
            Paragraph("<b>PORT & HARDWARE SECURITY COMPLIANCE AUDIT REPORT</b>", title_style),
            Paragraph(f"<b>CASE ID:</b> {report_id}<br/><b>DATE:</b> {timestamp}<br/><b>STATUS:</b> OFFICIAL AUDIT", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[360, 172])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=2, color=accent_blue, spaceBefore=4, spaceAfter=10))
    
    # 2. Executive Summary Box with Risk Badge
    score_p = Paragraph(
        f"<font size=28><b>{risk_data['net_risk']}</b></font><font size=12>/100</font><br/>"
        f"<b>NET RISK SCORE</b>",
        ParagraphStyle('ScoreStyle', parent=body_style, alignment=1, textColor=risk_hex)
    )
    
    summary_text = (
        f"<b>Audit Evaluation:</b> {scenario_name}<br/>"
        f"<b>Risk Classification:</b> <font color='{risk_hex.hexval()}'><b>{risk_level} RISK</b></font> (Raw Exposure: {risk_data['raw_risk']}, Mitigation Delta: -{risk_data['risk_delta']})<br/>"
        f"<b>Executive Verdict:</b> {risk_data['summary_verdict']}<br/>"
        f"<b>Audited Organization:</b> {organization_name} | <b>Assigned Auditor:</b> {auditor_name}"
    )
    summary_p = Paragraph(summary_text, body_style)
    
    exec_table = Table([[score_p, summary_p]], colWidths=[120, 412])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 10))
    
    # 3. Parameter Audit Matrix
    story.append(Paragraph("1. Audited Hardware & Environment Parameters", h2_style))
    param_data = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Configured Value</b>", body_style), Paragraph("<b>Risk Multiplier / Base</b>", body_style)],
        [Paragraph("Target Storage Device", body_style), Paragraph(device_type, body_style), Paragraph(f"Base: {risk_data.get('dimensions', {}).get('Exfiltration Hazard', 'N/A')}", body_style)],
        [Paragraph("Physical Port Interface", body_style), Paragraph(port_interface, body_style), Paragraph(f"Base: {risk_data.get('dimensions', {}).get('Network Bridging / Lateral', 'N/A')}", body_style)],
        [Paragraph("Physical Environment", body_style), Paragraph(environment, body_style), Paragraph(f"x{risk_data['multipliers']['Environment']}", body_style)],
        [Paragraph("User Privilege Level", body_style), Paragraph(user_privilege, body_style), Paragraph(f"x{risk_data['multipliers']['User Privilege']}", body_style)],
        [Paragraph("Data Classification", body_style), Paragraph(data_classification, body_style), Paragraph(f"x{risk_data['multipliers']['Data Sensitivity']}", body_style)],
        [Paragraph("Intended Action", body_style), Paragraph(intended_action, body_style), Paragraph(f"x{risk_data['multipliers']['Action Type']}", body_style)],
    ]
    param_table = Table(param_data, colWidths=[150, 242, 140])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 10))
    
    # 4. Dimensional Hazard Sub-Scores
    story.append(Paragraph("2. Dimensional Threat & Sub-Hazard Breakdown", h2_style))
    dim_data = [[Paragraph("<b>Hazard Vector</b>", body_style), Paragraph("<b>Sub-Score (0-100)</b>", body_style), Paragraph("<b>Vector Assessment</b>", body_style)]]
    
    for vec, score in risk_data["dimensions"].items():
        v_status = "CRITICAL" if score >= 75 else ("HIGH" if score >= 50 else ("MEDIUM" if score >= 25 else "LOW"))
        dim_data.append([
            Paragraph(vec, body_style),
            Paragraph(f"<b>{score}</b>/100", body_style),
            Paragraph(f"Status: <b>{v_status}</b>", body_style)
        ])
        
    dim_table = Table(dim_data, colWidths=[180, 110, 242])
    dim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(dim_table)
    story.append(Spacer(1, 10))
    
    # 5. Active Mitigations & Risk Reduction
    story.append(Paragraph("3. Active Technical & Administrative Mitigations Evaluated", h2_style))
    if risk_data["active_mitigations"]:
        mit_data = [[Paragraph("<b>Mitigation Control</b>", body_style), Paragraph("<b>Category</b>", body_style), Paragraph("<b>Credit Applied</b>", body_style)]]
        for m in risk_data["active_mitigations"]:
            mit_data.append([
                Paragraph(m["name"], body_style),
                Paragraph(m["category"], body_style),
                Paragraph(f"-{m['credit']} pts", body_style)
            ])
        mit_table = Table(mit_data, colWidths=[270, 130, 132])
        mit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(mit_table)
    else:
        story.append(Paragraph("<i>No active mitigations were toggled for this assessment baseline. Maximum gross exposure active.</i>", body_style))
    
    story.append(Spacer(1, 12))
    story.append(PageBreak())
    
    # 6. NIST SP 800-88 Rev. 1 Sanitization Directive
    story.append(Paragraph("4. NIST SP 800-88 Rev. 1 Media Sanitization Directive", h2_style))
    proto = sanitization_data["protocol"]
    
    nist_summary_data = [
        [Paragraph("<b>Target Media Category</b>", body_style), Paragraph(sanitization_data["media_category"], body_style)],
        [Paragraph("<b>Recommended Level</b>", body_style), Paragraph(f"<b>NIST SP 800-88 {sanitization_data['recommended_level']}</b>", body_style)],
        [Paragraph("<b>Required Protocol Method</b>", body_style), Paragraph(proto["method"], body_style)],
        [Paragraph("<b>Method Description</b>", body_style), Paragraph(proto["description"], body_style)],
        [Paragraph("<b>Verification Requirement</b>", body_style), Paragraph(proto["verification"], body_style)],
        [Paragraph("<b>Compliance Rationale</b>", body_style), Paragraph(sanitization_data["rationale"], body_style)],
    ]
    nist_table = Table(nist_summary_data, colWidths=[160, 372])
    nist_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(nist_table)
    story.append(Spacer(1, 12))
    
    # 7. Regulatory Framework Compliance Table
    story.append(Paragraph("5. Regulatory Framework Compliance Mapping", h2_style))
    comp_data = [[Paragraph("<b>Framework & Control</b>", body_style), Paragraph("<b>Control Title</b>", body_style), Paragraph("<b>Status</b>", body_style)]]
    
    for c in compliance_results[:6]:
        c_status_hex = colors.HexColor(c["status_color"])
        comp_data.append([
            Paragraph(f"<b>{c['framework']}</b><br/>{c['control_id']}", body_style),
            Paragraph(c["control_title"], body_style),
            Paragraph(f"<font color='{c_status_hex.hexval()}'><b>{c['status']}</b></font>", body_style)
        ])
        
    comp_table = Table(comp_data, colWidths=[150, 262, 120])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 14))

    # 8. Technical Remediation Snippet
    story.append(Paragraph("6. Required Technical Remediation Playbook (Excerpts)", h2_style))
    cisco_short = "\n".join([line for line in cisco_commands.split("\n") if line and not line.startswith("! ")][:8])
    ps_short = "\n".join([line for line in ps_scripts["usb_disable_ps"].split("\n") if line and not line.startswith("#")][:6])
    
    tech_data = [
        [Paragraph("<b>Layer-2 Switchport Security (Cisco IOS)</b>", body_style), Paragraph("<b>Windows Group Policy / PowerShell Script</b>", body_style)],
        [
            Paragraph(f"<font face='Courier' size=6.5>{cisco_short.replace(chr(10), '<br/>')}</font>", code_style),
            Paragraph(f"<font face='Courier' size=6.5>{ps_short.replace(chr(10), '<br/>')}</font>", code_style)
        ]
    ]
    tech_table = Table(tech_data, colWidths=[266, 266])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 16))
    
    # 9. Auditor Sign-Off & Verification Seal
    story.append(Paragraph("7. Auditor Attestation & Digital Verification Seal", h2_style))
    sign_text = (
        f"This policy compliance audit report was generated automatically by the <b>Hardware & Network Port Security Policy Auditor Decision Engine</b>. "
        f"The findings, calculated scores, and remediation measures represent an objective risk assessment conducted in accordance with "
        f"NIST SP 800-53 Rev. 5, NIST SP 800-88 Rev. 1, CIS Controls v8, and ISO/IEC 27001:2022.<br/><br/>"
        f"<b>Digital Signature Hash (SHA-256):</b> <code>{hashlib.sha256(f'{report_id}-{timestamp}'.encode()).hexdigest()}</code><br/>"
        f"<b>Compliance Officer:</b> {auditor_name} &nbsp;&nbsp;&nbsp;&nbsp; <b>Authorized Date:</b> {timestamp[:10]}"
    )
    sign_table = Table([[Paragraph(sign_text, body_style)]], colWidths=[532])
    sign_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, accent_blue),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sign_table)
    
    # Build Document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def generate_markdown_report(
    scenario_name: str,
    device_type: str,
    port_interface: str,
    environment: str,
    user_privilege: str,
    data_classification: str,
    intended_action: str,
    risk_data: Dict[str, Any],
    sanitization_data: Dict[str, Any],
    cisco_commands: str,
    ps_scripts: Dict[str, str],
    compliance_results: List[Dict[str, Any]],
    auditor_name: str = "Chief Information Security Officer (CISO)",
    organization_name: str = "Enterprise Global Security Operations"
) -> str:
    """Generates structured Markdown report for export or GRC integration."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_id = f"AUD-{hashlib.sha256(f'{scenario_name}{timestamp}'.encode()).hexdigest()[:10].upper()}"
    
    md = f"""# Hardware & Network Port Security Policy Audit Report

**Case Identifier:** `{report_id}`  
**Audit Timestamp:** `{timestamp}`  
**Organization:** {organization_name}  
**Lead Auditor:** {auditor_name}  

---

## 1. Executive Summary

- **Evaluated Scenario:** {scenario_name}
- **Net Security Risk Score:** **{risk_data['net_risk']} / 100**
- **Risk Level:** **{risk_data['risk_level']}**
- **Raw Exposure (Unmitigated):** {risk_data['raw_risk']} / 100
- **Mitigation Credit Delta:** -{risk_data['risk_delta']} points
- **Policy Verdict:** {risk_data['summary_verdict']}

### Dimensional Threat Breakdown
- **Exfiltration Hazard:** {risk_data['dimensions']['Exfiltration Hazard']} / 100
- **Rogue Device / BadUSB Injection:** {risk_data['dimensions']['Rogue Insertion (BadUSB/HID)']} / 100
- **Network Bridging & Lateral Movement:** {risk_data['dimensions']['Network Bridging / Lateral']} / 100
- **Physical Media Loss & Tampering:** {risk_data['dimensions']['Physical Media Loss / Tamper']} / 100

---

## 2. Audited Scenario Parameters

| Parameter Category | Configured Setting | Multiplier / Base Value |
|:---|:---|:---|
| **Storage Device** | {device_type} | Base Dimension: {risk_data['dimensions']['Exfiltration Hazard']} |
| **Physical Interface** | {port_interface} | Base Dimension: {risk_data['dimensions']['Network Bridging / Lateral']} |
| **Physical Environment** | {environment} | Multiplier: x{risk_data['multipliers']['Environment']} |
| **User Privilege Level** | {user_privilege} | Multiplier: x{risk_data['multipliers']['User Privilege']} |
| **Data Classification** | {data_classification} | Multiplier: x{risk_data['multipliers']['Data Sensitivity']} |
| **Intended Action** | {intended_action} | Multiplier: x{risk_data['multipliers']['Action Type']} |

---

## 3. NIST SP 800-88 Rev. 1 Media Sanitization Directive

- **Media Classification:** {sanitization_data['media_category']}
- **Required Sanitization Level:** **{sanitization_data['recommended_level']}**
- **Recommended Method:** `{sanitization_data['protocol']['method']}`
- **Technical Description:** {sanitization_data['protocol']['description']}
- **Verification Requirement:** {sanitization_data['protocol']['verification']}
- **Compliance Rationale:** {sanitization_data['rationale']}

---

## 4. Layer-2 Cisco Switchport Security Playbook

```cisco
{cisco_commands}
```

---

## 5. Windows PowerShell & Group Policy Remediation

```powershell
{ps_scripts['usb_disable_ps']}
```

---

## 6. Standards & Regulatory Compliance Matrix

| Framework | Control ID | Control Title | Status |
|:---|:---|:---|:---|
"""
    for c in compliance_results:
        md += f"| {c['framework']} | `{c['control_id']}` | {c['control_title']} | **{c['status']}** |\n"

    md += f"""
---

## 7. Attestation & Sign-off

- **Auditor Signature:** {auditor_name}
- **Integrity Hash:** `{hashlib.sha256(f'{report_id}-{timestamp}'.encode()).hexdigest()}`
- **Standard Baseline:** NIST SP 800-53 Rev. 5, NIST SP 800-88 Rev. 1, CIS Controls v8, ISO/IEC 27001:2022
"""
    return md
