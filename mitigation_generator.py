"""
Dynamic Remediation and Mitigation Generator for Hardware & Port Security.
Produces copy-ready PowerShell scripts, Windows GPO configurations,
Cisco IOS Layer-2 Switchport commands, Linux udev/usbguard policies,
and administrative control playbooks based on evaluated risk.
"""

from typing import Dict, List, Any


def generate_powershell_scripts(device_type: str, port_interface: str, net_risk: float) -> Dict[str, str]:
    """Generates automated PowerShell configuration scripts tailored to the scenario."""
    
    # 1. USB Storage Restriction Script
    usb_disable_ps = """# ==============================================================================
# SEC-SCRIPT: Enforce Immediate USB Removable Mass Storage Lockout
# Applies to: Windows 10/11 Enterprise & Windows Server 2016/2019/2022
# ==============================================================================

# 1. Modify USBSTOR Driver Startup Type (4 = Disabled, 3 = Manual/Default)
Write-Host "[+] Locking USBSTOR driver startup in registry..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR" -Name "Start" -Value 4 -Type DWord -Force

# 2. Block Storage Device Installation via Device Class Policies
$DevicePolicyPath = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeviceInstall\\Restrictions"
If (!(Test-Path $DevicePolicyPath)) {
    New-Item -Path $DevicePolicyPath -Force | Out-Null
}
# Deny devices not specifically allowed by admin
Set-ItemProperty -Path $DevicePolicyPath -Name "DenyUnspecified" -Value 1 -Type DWord -Force

# 3. Enable Detailed Removable Storage Access Auditing (Event ID 4663 / 4656)
Write-Host "[+] Enabling detailed audit subcategories for Removable Storage..." -ForegroundColor Cyan
auditpol /set /subcategory:"Removable Storage" /success:enable /failure:enable

Write-Host "[SUCCESS] USB Storage interface successfully locked down on $(hostname)." -ForegroundColor Green
"""

    # 2. USB Read-Only Mode Script
    usb_readonly_ps = """# ==============================================================================
# SEC-SCRIPT: Enforce Read-Only Mode for External Storage (Anti-Exfiltration)
# Prevents writing data to external USBs/SSDs while allowing read operations
# ==============================================================================

$StoragePolicyPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\StorageDevicePolicies"

If (!(Test-Path $StoragePolicyPath)) {
    New-Item -Path $StoragePolicyPath -Force | Out-Null
}

Write-Host "[+] Enforcing WriteProtect=1 on StorageDevicePolicies..." -ForegroundColor Cyan
Set-ItemProperty -Path $StoragePolicyPath -Name "WriteProtect" -Value 1 -Type DWord -Force

Write-Host "[SUCCESS] Read-Only policy active. External mass storage writes are blocked." -ForegroundColor Green
"""

    # 3. DMA / Thunderbolt Direct Access Protection Script
    thunderbolt_dma_ps = """# ==============================================================================
# SEC-SCRIPT: Kernel DMA Protection & External Thunderbolt PCIe Security
# Mitigates Physical DMA Drive-by Attacks (e.g., PCILeech)
# ==============================================================================

$DmaPolicyPath = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\KernelDMAProtection"
If (!(Test-Path $DmaPolicyPath)) {
    New-Item -Path $DmaPolicyPath -Force | Out-Null
}

# Enforce DMA port security level: 1 = Enforce DMA Remapping for Thunderbolt
Set-ItemProperty -Path $DmaPolicyPath -Name "DeviceEnumerationPolicy" -Value 1 -Type DWord -Force

# Disable BitLocker DMA debugging exposure
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\FVE" -Name "DisableExternalDMAUnderLock" -Value 1 -Type DWord -Force

Write-Host "[SUCCESS] Kernel DMA Protection and Thunderbolt enumeration policies enforced." -ForegroundColor Green
"""

    # 4. BitLocker Drive Encryption Command
    bitlocker_ps = """# ==============================================================================
# SEC-SCRIPT: Verify and Enforce BitLocker AES-256 Encryption
# ==============================================================================

$DriveLetter = "E:" # Target Removable or Fixed Volume
Write-Host "[+] Checking BitLocker status on $DriveLetter..." -ForegroundColor Cyan

$Volume = Get-BitLockerVolume -MountPoint $DriveLetter -ErrorAction SilentlyContinue
if ($Volume -and $Volume.VolumeStatus -ne 'FullyEncrypted') {
    Write-Host "[!] Drive is not fully encrypted. Enabling BitLocker with AES-256..." -ForegroundColor Yellow
    Enable-BitLocker -MountPoint $DriveLetter -EncryptionMethod XtsAes256 -UsedSpaceOnly -PasswordProtector
} else {
    Write-Host "[+] Volume $DriveLetter is fully encrypted or verified." -ForegroundColor Green
}
"""

    return {
        "usb_disable_ps": usb_disable_ps,
        "usb_readonly_ps": usb_readonly_ps,
        "thunderbolt_dma_ps": thunderbolt_dma_ps,
        "bitlocker_ps": bitlocker_ps
    }


def generate_cisco_switchport_commands(port_interface: str, net_risk: float) -> str:
    """Generates production-grade Cisco IOS Layer-2 Port Security CLI snippet."""
    
    violation_action = "shutdown" if net_risk >= 60.0 else "restrict"
    
    cisco_cli = f"""! ==============================================================================
! CISCO IOS / CATALYST SWITCH LAYER-2 PORT SECURITY CONFIGURATION
! Applied Interface: GigabitEthernet1/0/24 (Target Physical Port)
! Policy Action on Violation: {violation_action.upper()}
! ==============================================================================

configure terminal
interface GigabitEthernet1/0/24
 description SECURED_CLIENT_ACCESS_PORT

 ! 1. Force access port mode (prevent VLAN hopping trunk negotiation)
 switchport mode access
 switchport access vlan 10
 switchport nonegotiate

 ! 2. Activate Layer-2 Port Security
 switchport port-security

 ! 3. Restrict port to exactly 1 authorized MAC address
 switchport port-security maximum 1

 ! 4. Learn and bind the connecting device MAC dynamically to startup-config
 switchport port-security mac-address sticky

 ! 5. Set violation mode (Shutdown port immediately if unapproved MAC connects)
 switchport port-security violation {violation_action}

 ! 6. Enable STP Edge Port & BPDU Guard to prevent rogue switches / bridges
 spanning-tree portfast
 spanning-tree bpduguard enable

 ! 7. Enable Storm Control to prevent broadcast flood exfiltration / DoS
 storm-control broadcast level 2.0
 storm-control action trap

 ! 8. (Optional) Configure 802.1X Authenticator with MAB Fallback
 ! dot1x pae authenticator
 ! dot1x port-control auto
 ! mab

 exit
write memory
"""
    return cisco_cli


def generate_linux_rules() -> Dict[str, str]:
    """Generates Linux udev and usbguard configuration rules."""
    
    udev_rule = """# ==============================================================================
# Linux udev Rule: Block all newly inserted USB Mass Storage devices
# Location: /etc/udev/rules.d/99-block-usb-storage.rules
# ==============================================================================

# Match USB mass storage driver (bInterfaceClass 08) and de-authorize
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{bInterfaceClass}=="08", ATTR{authorized}="0"

# Log security violation to system journal
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{bInterfaceClass}=="08", RUN+="/usr/bin/logger -p authpriv.alert '[SEC-ALERT] Unauthorized USB Storage device insertion blocked: %k'"
"""

    usbguard_policy = """# ==============================================================================
# Linux USBGuard Rule Baseline: Restrict USB Peripherals
# Location: /etc/usbguard/rules.conf
# ==============================================================================

# Allow internal system root hub controllers
allow with-interface equals { 09:00:00 }

# Allow authorized HID keyboard and mice only
allow with-interface equals { 03:01:01 03:01:02 }

# Block mass storage interfaces unconditionally
block with-interface equals { 08:*:* }

# Block all unclassified or multi-function badUSB devices
block id *:*
"""
    return {
        "udev_rule": udev_rule,
        "usbguard_policy": usbguard_policy
    }


def get_actionable_remediation_summary(risk_data: Dict[str, Any], device_type: str, port_interface: str) -> List[Dict[str, str]]:
    """Returns structured, prioritized technical and administrative remediation measures."""
    net_risk = risk_data["net_risk"]
    remediations = []

    if "USB" in port_interface or "Flash" in device_type or "SSD" in device_type:
        remediations.append({
            "category": "Endpoint Group Policy",
            "priority": "HIGH" if net_risk >= 60 else "MEDIUM",
            "title": "Enforce Removable Storage GPO Restriction",
            "detail": "Deploy Active Directory Group Policy setting 'All Removable Storage classes: Deny all access' or configure Read-Only access if business ingestion is required."
        })
        remediations.append({
            "category": "Host Antivirus & EDR",
            "priority": "HIGH",
            "title": "Real-time Removable Drive Auto-Scan",
            "detail": "Configure Windows Defender / CrowdStrike Falcon to execute immediate background heuristic scans upon USB insertion events."
        })

    if "Ethernet" in port_interface or "Console" in port_interface:
        remediations.append({
            "category": "Network Infrastructure",
            "priority": "CRITICAL" if net_risk >= 60 else "HIGH",
            "title": "Enable Layer-2 Switchport Security & BPDU Guard",
            "detail": "Apply `switchport port-security mac-address sticky` with `violation shutdown` on Cisco/Aruba switches to prevent rogue device bridging."
        })
        remediations.append({
            "category": "Network Access Control",
            "priority": "HIGH",
            "title": "Deploy 802.1X EAP-TLS Authentication",
            "detail": "Require RADIUS machine certificates for network transit. Unauthenticated devices should be placed into an isolated guest quarantine VLAN."
        })

    if "Thunderbolt" in port_interface:
        remediations.append({
            "category": "Hardware & Kernel",
            "priority": "CRITICAL",
            "title": "Enforce Kernel DMA Protection in UEFI",
            "detail": "Enable Intel VT-d / AMD IOMMU in BIOS and set Windows Kernel DMA Protection policy to block direct memory exfiltration attacks."
        })

    if net_risk >= 50:
        remediations.append({
            "category": "Physical Security",
            "priority": "HIGH",
            "title": "Deploy Keyed Physical Port Blockers",
            "detail": "Install mechanical RJ45 and USB jack blockers into physical ports located in shared and public areas to physically eliminate plug-in opportunity."
        })
        remediations.append({
            "category": "SIEM & SOC",
            "priority": "MEDIUM",
            "title": "Configure Syslog Alerts for Port Violations",
            "detail": "Stream Event ID 20001 (PnP device connect) and switchport violation Syslog traps directly to Splunk/Sentinel with automated ticket dispatch."
        })

    return remediations
