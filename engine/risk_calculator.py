"""
Weighted Risk Calculation Engine for Hardware & Network Port Security Policy Auditor.
Calculates objective Security Risk Scores (0-100), dimensional hazard breakdown,
and evaluates net risk reduction based on active technical/administrative mitigations.
"""

from typing import Dict, List, Any, Tuple


# Base Risk Values for Storage Devices (0-100)
DEVICE_BASE_RISK: Dict[str, float] = {
    "USB Flash Drive (Removable Mass Storage)": 75.0,
    "External SSD (USB-C / NVMe Enclosure)": 70.0,
    "High-Performance Internal NVMe / PCIe SSD": 55.0,
    "External Magnetic HDD (Mechanical Storage)": 60.0,
    "Enterprise NAS Appliance (NFS / SMB / iSCSI)": 50.0,
    "SAN Fibre Channel Fabric / LUN Array": 45.0,
    "Removable MicroSD / SD Card": 78.0,
    "Legacy Magnetic Tape Cartridge (LTO)": 40.0,
}

# Base Risk Values for Physical Port Interfaces (0-100)
PORT_BASE_RISK: Dict[str, float] = {
    "USB 3.2 / USB-C Port (High Speed / DMA Capable)": 72.0,
    "USB 2.0 Legacy Port (Standard Mass Storage)": 65.0,
    "Ethernet RJ45 LAN Socket (Layer-2 Access Port)": 68.0,
    "Serial / RS-232 / RJ45 Console Management Port": 80.0,
    "Fibre Channel SFP+ / QSFP Optical Port": 45.0,
    "Thunderbolt 3/4 Port (Direct PCIe DMA Access)": 88.0,
    "DisplayPort / HDMI (With Aux / Sideband Channel)": 42.0,
}

# Environment Risk Multipliers
ENVIRONMENT_MULTIPLIERS: Dict[str, float] = {
    "Public Reception / Unmonitored Lobby": 1.45,
    "Open-Plan Corporate Office Floor": 1.15,
    "Executive Boardroom / Conference Room": 1.05,
    "Server Room / Tier-3 Data Center (Access Controlled)": 0.70,
    "Field Operation / Remote Unattended Site": 1.40,
    "High-Security SCIF / Restricted R&D Vault": 0.55,
}

# User Privilege Level Multipliers (Higher = Greater Risk if unvetted/adversarial)
PRIVILEGE_MULTIPLIERS: Dict[str, float] = {
    "Guest / Unverified Visitor": 1.50,
    "Student / Temporary Intern": 1.25,
    "Contractor / Third-Party Vendor": 1.20,
    "Standard Corporate Employee": 1.00,
    "IT Systems / Network Administrator (Privileged)": 0.85,
    "Certified Security Auditor / Compliance Officer": 0.75,
}

# Data Classification Multipliers
DATA_CLASSIFICATION_MULTIPLIERS: Dict[str, float] = {
    "Public / Unclassified Data (Low Impact)": 0.75,
    "Internal Business Operational Data": 1.00,
    "Confidential Proprietary / Customer Data": 1.25,
    "Restricted / Secret Intellectual Property": 1.45,
    "Regulated PII / HIPAA / Financial (PCI-DSS)": 1.50,
}

# Intended Action Multipliers
ACTION_MULTIPLIERS: Dict[str, float] = {
    "Routine Workstation Read/Write Storage Access": 1.00,
    "Temporary Diagnostic / Maintenance Hotplug": 1.15,
    "Hardware Re-assignment Between Users/Depts": 1.10,
    "Cross-Environment High-Low Data Migration": 1.35,
    "End-of-Life Decommissioning / Hardware Disposal": 1.30,
}

# Mitigation Definitions with Credit Scores and dimensional effectiveness
ACTIVE_MITIGATIONS_DEF: Dict[str, Dict[str, Any]] = {
    "mac_binding": {
        "name": "Layer-2 Switch MAC Address Binding & Port Security",
        "category": "Network",
        "credit": 18.0,
        "description": "Enforces sticky MAC limits and port shutdown violation mode on physical switchports.",
        "targets": ["network_bridging", "rogue_device"]
    },
    "nac_8021x": {
        "name": "802.1X Network Access Control (NAC) & Dynamic VLAN",
        "category": "Network",
        "credit": 16.0,
        "description": "Requires cryptographic EAP-TLS certificate before granting switchport network transit.",
        "targets": ["network_bridging", "rogue_device"]
    },
    "usb_gpo_block": {
        "name": "Endpoint Group Policy (GPO) Full USB Storage Disablement",
        "category": "Endpoint",
        "credit": 24.0,
        "description": "Sets USBSTOR service startup to 4 (Disabled) via Active Directory Central GPO.",
        "targets": ["exfiltration", "malware_insertion"]
    },
    "usb_gpo_readonly": {
        "name": "Endpoint GPO Storage Write-Protection (Read-Only Mode)",
        "category": "Endpoint",
        "credit": 15.0,
        "description": "Enforces WriteProtect=1 on StorageDevicePolicies to allow input while blocking exfiltration.",
        "targets": ["exfiltration"]
    },
    "endpoint_dlp": {
        "name": "Endpoint Data Loss Prevention (DLP) & Device Control Agent",
        "category": "Endpoint",
        "credit": 14.0,
        "description": "Inspects file contents and hashes in real-time before allowing transfers to external media.",
        "targets": ["exfiltration"]
    },
    "port_physical_locks": {
        "name": "Physical Port Locks & RJ45/USB Jack Blockers",
        "category": "Physical",
        "credit": 12.0,
        "description": "Keyed mechanical locks physically installed into unused RJ45 and USB slots.",
        "targets": ["physical_tamper", "rogue_device"]
    },
    "device_encryption": {
        "name": "Hardware-Level Full Disk Encryption (BitLocker / LUKS / OPAL SED)",
        "category": "Hardware",
        "credit": 16.0,
        "description": "AES-XTS 256-bit encryption ensuring data-at-rest protection if drive is lost or stolen.",
        "targets": ["physical_tamper", "exfiltration"]
    },
    "siem_logging": {
        "name": "Real-Time Port Event Auditing & SIEM / SOC Alerting",
        "category": "Monitoring",
        "credit": 10.0,
        "description": "Streams Event ID 20001 (PnP plug) and switch Syslog traps to SOC with sub-second alert rules.",
        "targets": ["network_bridging", "rogue_device", "exfiltration"]
    },
    "bios_disable": {
        "name": "Firmware / UEFI BIOS Port Disablement & Admin Lock",
        "category": "Hardware",
        "credit": 15.0,
        "description": "Physically powers down controller logic at motherboard firmware level, secured by supervisor PIN.",
        "targets": ["rogue_device", "malware_insertion", "physical_tamper"]
    },
    "escorted_access": {
        "name": "Mandatory Two-Person Escort & Chain of Custody Protocol",
        "category": "Administrative",
        "credit": 10.0,
        "description": "Requires dual-signoff logbook and continuous visual supervision during hardware access.",
        "targets": ["physical_tamper", "rogue_device"]
    }
}


def calculate_risk(
    device_type: str,
    port_interface: str,
    environment: str,
    user_privilege: str,
    data_classification: str,
    intended_action: str,
    selected_mitigations: List[str]
) -> Dict[str, Any]:
    """
    Computes baseline risk, applied multipliers, mitigation deductions,
    net risk score (0-100), risk tier classification, and dimensional sub-hazards.
    """
    # 1. Base Hardware & Port Risk calculation (Harmonic weighted combination)
    dev_base = DEVICE_BASE_RISK.get(device_type, 60.0)
    port_base = PORT_BASE_RISK.get(port_interface, 60.0)
    base_combined = (0.55 * dev_base) + (0.45 * port_base)

    # 2. Extract Context Multipliers
    env_mult = ENVIRONMENT_MULTIPLIERS.get(environment, 1.0)
    priv_mult = PRIVILEGE_MULTIPLIERS.get(user_privilege, 1.0)
    data_mult = DATA_CLASSIFICATION_MULTIPLIERS.get(data_classification, 1.0)
    action_mult = ACTION_MULTIPLIERS.get(intended_action, 1.0)

    # Combined context coefficient
    combined_multiplier = env_mult * priv_mult * data_mult * action_mult
    
    # 3. Calculate Raw / Gross Risk Score
    raw_risk = base_combined * (combined_multiplier ** 0.65)
    raw_risk = max(0.0, min(100.0, raw_risk))

    # 4. Calculate Mitigation Credits
    total_mitigation_credit = 0.0
    active_mitigation_details = []
    
    # Check for mutual exclusivity / diminishing returns
    has_full_block = "usb_gpo_block" in selected_mitigations
    
    for mit_key in selected_mitigations:
        if mit_key in ACTIVE_MITIGATIONS_DEF:
            mit_info = ACTIVE_MITIGATIONS_DEF[mit_key]
            credit = mit_info["credit"]
            
            # If full block is active, read-only provides reduced marginal benefit
            if mit_key == "usb_gpo_readonly" and has_full_block:
                credit = credit * 0.2
                
            total_mitigation_credit += credit
            active_mitigation_details.append({
                "key": mit_key,
                "name": mit_info["name"],
                "category": mit_info["category"],
                "credit": credit
            })

    # Apply logarithmic dampening to extreme mitigation stacking
    effective_mitigation = total_mitigation_credit * (1.0 - (total_mitigation_credit / 300.0))
    
    # 5. Net Risk Calculation
    net_risk = raw_risk - effective_mitigation
    net_risk = round(max(0.0, min(100.0, net_risk)), 1)
    raw_risk = round(raw_risk, 1)
    risk_delta = round(raw_risk - net_risk, 1)

    # 6. Risk Tier & Assessment Classification
    if net_risk <= 29.9:
        risk_level = "LOW"
        risk_color = "#10b981"
        badge_class = "badge-low"
        summary_verdict = "AUTHORIZED OPERATIONAL STATE: Risk is within acceptable enterprise tolerance thresholds."
    elif net_risk <= 59.9:
        risk_level = "MEDIUM"
        risk_color = "#f59e0b"
        badge_class = "badge-med"
        summary_verdict = "CONDITIONAL APPROVAL REQUIRED: Moderate exposure detected. Verify identity and enforce standard mitigations."
    elif net_risk <= 84.9:
        risk_level = "HIGH"
        risk_color = "#f97316"
        badge_class = "badge-high"
        summary_verdict = "RESTRICTED ACCESS WARNING: Significant security exposure. Mandatory GPO / Port Security controls must be verified active."
    else:
        risk_level = "CRITICAL"
        risk_color = "#ef4444"
        badge_class = "badge-crit"
        summary_verdict = "PROHIBITED HAZARD STATE: Severe policy violation. Immediate automated port lockdown or physical disconnection required."

    # 7. Dimensional Sub-Hazard Analysis (0-100 scale each)
    # Exfiltration Hazard
    exfil_base = (dev_base * 0.6 + data_mult * 30.0) * (env_mult * 0.7)
    if "usb_gpo_block" in selected_mitigations:
        exfil_base *= 0.15
    elif "usb_gpo_readonly" in selected_mitigations:
        exfil_base *= 0.30
    if "endpoint_dlp" in selected_mitigations:
        exfil_base *= 0.55
    if "device_encryption" in selected_mitigations:
        exfil_base *= 0.75
    exfil_score = round(max(0.0, min(100.0, exfil_base)), 1)

    # Rogue Device & BadUSB / HID Insertion Hazard
    rogue_base = (port_base * 0.7 + priv_mult * 25.0) * (env_mult * 0.8)
    if "bios_disable" in selected_mitigations:
        rogue_base *= 0.10
    if "port_physical_locks" in selected_mitigations:
        rogue_base *= 0.35
    if "usb_gpo_block" in selected_mitigations:
        rogue_base *= 0.40
    if "mac_binding" in selected_mitigations and "Ethernet" in port_interface:
        rogue_base *= 0.25
    rogue_score = round(max(0.0, min(100.0, rogue_base)), 1)

    # Unauthorized Network Bridging & Lateral Movement
    is_network_port = "Ethernet" in port_interface or "Console" in port_interface or "NAS" in device_type or "SAN" in device_type
    bridge_base = (port_base * 0.8 + priv_mult * 20.0) if is_network_port else (port_base * 0.3)
    if "mac_binding" in selected_mitigations:
        bridge_base *= 0.25
    if "nac_8021x" in selected_mitigations:
        bridge_base *= 0.20
    if "siem_logging" in selected_mitigations:
        bridge_base *= 0.70
    bridge_score = round(max(0.0, min(100.0, bridge_base)), 1)

    # Physical Tampering & Media Loss Hazard
    tamper_base = (dev_base * 0.5 + env_mult * 35.0) * action_mult
    if "device_encryption" in selected_mitigations:
        tamper_base *= 0.30
    if "escorted_access" in selected_mitigations:
        tamper_base *= 0.35
    if "port_physical_locks" in selected_mitigations:
        tamper_base *= 0.55
    tamper_score = round(max(0.0, min(100.0, tamper_base)), 1)

    # 8. Dynamic Threat Tags Generation
    threat_tags = []
    if "Public" in environment or "Guest" in user_privilege:
        threat_tags.append("Unvetted Physical Access Exposure")
    if "Thunderbolt" in port_interface:
        threat_tags.append("Direct Memory Access (DMA) Bus Vulnerability")
    if "USB" in port_interface and not has_full_block:
        threat_tags.append("BadUSB / Rubber Ducky HID Injection Vector")
    if "Console" in port_interface and "Server" not in environment:
        threat_tags.append("Unprotected Out-of-Band Network Switch Console")
    if ("Confidential" in data_classification or "Regulated" in data_classification) and "device_encryption" not in selected_mitigations:
        threat_tags.append("Unencrypted High-Sensitivity Data at Rest")
    if "Decommissioning" in intended_action:
        threat_tags.append("Hardware Residual Data Sanitization Requirement")
    if "Ethernet" in port_interface and "mac_binding" not in selected_mitigations and "nac_8021x" not in selected_mitigations:
        threat_tags.append("Unauthenticated Layer-2 MAC Spoofing / Rogue AP Risk")

    return {
        "net_risk": net_risk,
        "raw_risk": raw_risk,
        "risk_delta": risk_delta,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "badge_class": badge_class,
        "summary_verdict": summary_verdict,
        "dimensions": {
            "Exfiltration Hazard": exfil_score,
            "Rogue Insertion (BadUSB/HID)": rogue_score,
            "Network Bridging / Lateral": bridge_score,
            "Physical Media Loss / Tamper": tamper_score,
        },
        "multipliers": {
            "Environment": env_mult,
            "User Privilege": priv_mult,
            "Data Sensitivity": data_mult,
            "Action Type": action_mult,
            "Combined Multiplier": round(combined_multiplier, 2)
        },
        "threat_tags": threat_tags,
        "active_mitigations": active_mitigation_details,
        "mitigation_credit_total": round(effective_mitigation, 1)
    }
