"""
Regulatory Framework Compliance Matrix for Port & Hardware Security.
Maps active controls and scenario configurations against NIST SP 800-53 Rev. 5,
CIS Controls v8, and ISO/IEC 27001:2022.
"""

from typing import Dict, List, Any


COMPLIANCE_CONTROLS: List[Dict[str, Any]] = [
    {
        "framework": "NIST SP 800-53 Rev. 5",
        "control_id": "MP-7",
        "control_title": "Media Use — Removable Media Controls",
        "description": "Restricts the use of physical removable storage media on systems unless explicitly authorized and scanned.",
        "mitigation_requirement": ["usb_gpo_block", "usb_gpo_readonly", "endpoint_dlp"],
        "guidance": "Enforce GPO USB block or Read-Only policies to prevent unauthorized data ingress/egress."
    },
    {
        "framework": "NIST SP 800-53 Rev. 5",
        "control_id": "MP-6",
        "control_title": "Media Sanitization",
        "description": "Sanitizes system media prior to disposal, release out of organizational control, or release for reuse.",
        "mitigation_requirement": ["device_encryption", "escorted_access"],
        "guidance": "Follow NIST SP 800-88 Rev. 1 Clear/Purge/Destroy directives based on media type."
    },
    {
        "framework": "NIST SP 800-53 Rev. 5",
        "control_id": "SC-7",
        "control_title": "Boundary Protection — Physical Port Security",
        "description": "Monitors and controls communications at external boundaries and physical interface switchports.",
        "mitigation_requirement": ["mac_binding", "nac_8021x", "port_physical_locks"],
        "guidance": "Configure Layer-2 switchport port-security, sticky MAC binding, and 802.1X NAC."
    },
    {
        "framework": "NIST SP 800-53 Rev. 5",
        "control_id": "IA-3",
        "control_title": "Device Identification & Authentication",
        "description": "Uniquely identifies and authenticates devices before establishing a physical or logical connection.",
        "mitigation_requirement": ["nac_8021x", "mac_binding"],
        "guidance": "Enforce 802.1X certificate-based machine authentication or MAC Authentication Bypass."
    },
    {
        "framework": "CIS Controls v8",
        "control_id": "CIS 10.3",
        "control_title": "Disable Removable Media Access",
        "description": "Disable the use of removable media interfaces unless approved with formal business exceptions.",
        "mitigation_requirement": ["usb_gpo_block", "bios_disable"],
        "guidance": "Deploy Active Directory GPOs setting USBSTOR to disabled (Start=4) on endpoint fleets."
    },
    {
        "framework": "CIS Controls v8",
        "control_id": "CIS 10.5",
        "control_title": "Enforce Hardware Full Disk Encryption",
        "description": "Ensure all storage media and removable storage devices enforce AES-256 BitLocker/LUKS encryption.",
        "mitigation_requirement": ["device_encryption"],
        "guidance": "Mandate hardware BitLocker or OPAL 2.0 SED encryption across all mobile storage assets."
    },
    {
        "framework": "CIS Controls v8",
        "control_id": "CIS 1.2",
        "control_title": "Address Unauthorized Assets",
        "description": "Ensure unauthorized devices connecting to network sockets are automatically isolated or blocked.",
        "mitigation_requirement": ["mac_binding", "nac_8021x"],
        "guidance": "Configure switchport violation shutdown to disable ports immediately upon rogue asset insertion."
    },
    {
        "framework": "ISO/IEC 27001:2022",
        "control_id": "A.7.10",
        "control_title": "Storage Media Lifecycle Management",
        "description": "Storage media shall be managed through its lifecycle of acquisition, use, transportation, and disposal.",
        "mitigation_requirement": ["device_encryption", "escorted_access"],
        "guidance": "Maintain chain of custody records and cryptographic protection during all storage transit."
    },
    {
        "framework": "ISO/IEC 27001:2022",
        "control_id": "A.7.14",
        "control_title": "Secure Disposal or Re-use of Equipment",
        "description": "Items of equipment containing storage media shall be verified to ensure any sensitive data has been sanitized.",
        "mitigation_requirement": ["device_encryption"],
        "guidance": "Issue verifiable NIST SP 800-88 certificates of sanitization prior to equipment re-use or disposal."
    },
    {
        "framework": "ISO/IEC 27001:2022",
        "control_id": "A.8.20",
        "control_title": "Network Security & Physical Access Binding",
        "description": "Networks and network devices shall be secured, managed, and controlled to protect information.",
        "mitigation_requirement": ["mac_binding", "nac_8021x", "siem_logging"],
        "guidance": "Apply strict Layer-2 MAC controls and stream connection audit events to SIEM in real time."
    }
]


def evaluate_compliance_matrix(active_mitigations: List[str]) -> List[Dict[str, Any]]:
    """
    Evaluates the compliance matrix against active mitigations in the current scenario.
    Returns compliance status (COMPLIANT, PARTIAL, NON-COMPLIANT) for each standard.
    """
    results = []
    
    for ctrl in COMPLIANCE_CONTROLS:
        reqs = ctrl["mitigation_requirement"]
        matched = [m for m in reqs if m in active_mitigations]
        
        if len(matched) == len(reqs) or (len(reqs) > 1 and len(matched) >= 1 and ("usb_gpo_block" in matched or "mac_binding" in matched)):
            status = "COMPLIANT"
            status_color = "#10b981"
            status_badge = "badge-low"
        elif len(matched) > 0:
            status = "PARTIAL"
            status_color = "#f59e0b"
            status_badge = "badge-med"
        else:
            status = "NON-COMPLIANT"
            status_color = "#ef4444"
            status_badge = "badge-crit"
            
        results.append({
            "framework": ctrl["framework"],
            "control_id": ctrl["control_id"],
            "control_title": ctrl["control_title"],
            "description": ctrl["description"],
            "guidance": ctrl["guidance"],
            "matched_mitigations": matched,
            "required_mitigations": reqs,
            "status": status,
            "status_color": status_color,
            "status_badge": status_badge
        })
        
    return results
