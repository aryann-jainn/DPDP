"""
Preset Real-World Scenarios for Port Security Policy Auditor.
Enables rapid one-click demonstration of high-risk, operational, and decommissioning use cases.
"""

from typing import Dict, Any


PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Select a Custom Scenario...": {
        "device_type": "USB Flash Drive (Removable Mass Storage)",
        "port_interface": "USB 3.2 / USB-C Port (High Speed / DMA Capable)",
        "environment": "Open-Plan Corporate Office Floor",
        "user_privilege": "Standard Corporate Employee",
        "data_classification": "Internal Business Operational Data",
        "intended_action": "Routine Workstation Read/Write Storage Access",
        "mitigations": [],
        "description": "Clean default template for custom parameter selection."
    },
    "🚨 Scenario 1: Rogue Guest USB in Unattended Reception Socket": {
        "device_type": "USB Flash Drive (Removable Mass Storage)",
        "port_interface": "USB 3.2 / USB-C Port (High Speed / DMA Capable)",
        "environment": "Public Reception / Unmonitored Lobby",
        "user_privilege": "Guest / Unverified Visitor",
        "data_classification": "Confidential Proprietary / Customer Data",
        "intended_action": "Temporary Diagnostic / Maintenance Hotplug",
        "mitigations": [],
        "description": "High-risk scenario: An unescorted visitor plugs an untrusted USB rubber ducky or flash drive into an open lobby kiosk terminal with zero active mitigations."
    },
    "♻️ Scenario 2: Decommissioning Enterprise SAN SSD Array (Financial Data)": {
        "device_type": "SAN Fibre Channel Fabric / LUN Array",
        "port_interface": "Fibre Channel SFP+ / QSFP Optical Port",
        "environment": "Server Room / Tier-3 Data Center (Access Controlled)",
        "user_privilege": "IT Systems / Network Administrator (Privileged)",
        "data_classification": "Regulated PII / HIPAA / Financial (PCI-DSS)",
        "intended_action": "End-of-Life Decommissioning / Hardware Disposal",
        "mitigations": ["device_encryption", "escorted_access", "siem_logging"],
        "description": "Storage lifecycle scenario: Retiring a multi-terabyte flash array storing regulated PCI-DSS cardholder data. Requires NIST SP 800-88 Purge/Destroy protocols."
    },
    "🔌 Scenario 3: Untrusted Contractor Laptop on Data Center Ethernet": {
        "device_type": "High-Performance Internal NVMe / PCIe SSD",
        "port_interface": "Ethernet RJ45 LAN Socket (Layer-2 Access Port)",
        "environment": "Server Room / Tier-3 Data Center (Access Controlled)",
        "user_privilege": "Contractor / Third-Party Vendor",
        "data_classification": "Restricted / Secret Intellectual Property",
        "intended_action": "Temporary Diagnostic / Maintenance Hotplug",
        "mitigations": [],
        "description": "Network exposure scenario: An external HVAC vendor or contractor plugs a personal laptop directly into a server rack Ethernet switchport without 802.1X NAC or MAC binding."
    },
    "💻 Scenario 4: Corporate Laptop Re-assignment with BitLocker Active": {
        "device_type": "External SSD (USB-C / NVMe Enclosure)",
        "port_interface": "USB 3.2 / USB-C Port (High Speed / DMA Capable)",
        "environment": "Open-Plan Corporate Office Floor",
        "user_privilege": "Standard Corporate Employee",
        "data_classification": "Internal Business Operational Data",
        "intended_action": "Hardware Re-assignment Between Users/Depts",
        "mitigations": ["usb_gpo_readonly", "device_encryption", "endpoint_dlp", "siem_logging"],
        "description": "Managed corporate scenario: Standard hardware handoff between engineering departments with endpoint DLP, Read-Only USB policy, and BitLocker active."
    },
    "⚡ Scenario 5: Remote SCADA Switch Console Port Maintenance": {
        "device_type": "External Magnetic HDD (Mechanical Storage)",
        "port_interface": "Serial / RS-232 / RJ45 Console Management Port",
        "environment": "Field Operation / Remote Unattended Site",
        "user_privilege": "Contractor / Third-Party Vendor",
        "data_classification": "Confidential Proprietary / Customer Data",
        "intended_action": "Temporary Diagnostic / Maintenance Hotplug",
        "mitigations": ["port_physical_locks"],
        "description": "Industrial control scenario: Direct serial console access at an unmonitored substation switch without 2-person escort or dual authentication."
    }
}
