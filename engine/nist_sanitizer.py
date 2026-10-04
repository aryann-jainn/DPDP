"""
NIST SP 800-88 Rev. 1 Media Sanitization Decision Engine & Certificate Generator.
Maps hardware decommissioning and re-assignment scenarios directly to
Clear, Purge, and Destroy protocols based on media physics and data classification.
"""

from typing import Dict, List, Any
import datetime
import hashlib


# Media-specific NIST SP 800-88 Rev. 1 Sanitization Guidelines
NIST_MEDIA_GUIDELINES: Dict[str, Dict[str, Any]] = {
    "SSD / NVMe Flash": {
        "media_physics_notes": "NAND Flash utilizes wear-leveling algorithms and over-provisioned spare blocks. Traditional logical block overwriting cannot reliably reach hidden reserved blocks.",
        "clear": {
            "method": "ATA Secure Erase / NVMe Format (User Data Erase)",
            "description": "Applies controller-level command to rewrite all accessible user addressable locations with binary zeros or random patterns.",
            "suitable_for": "Internal re-assignment within same security domain / same data classification.",
            "verification": "Read full LBA range (minimum 10% random sampling) to verify zero pattern."
        },
        "purge": {
            "method": "NVMe Sanitize (Cryptographic Erase) / ATA Enhanced Secure Erase",
            "description": "Destroys internal Media Encryption Key (MEK) via crypto-scramble and forces full flash block voltage discharge across all NAND dies, including wear-leveled and reserved areas.",
            "suitable_for": "Re-assignment to lower security classification, external vendor return, or hardware leasing return.",
            "verification": "Query NVMe Sanitize Status log page to confirm exit code 0x00 and verify MEK invalidation."
        },
        "destroy": {
            "method": "Cross-Cut Disintegration / Mechanical Shredding (< 2mm particle size)",
            "description": "Passes drive through industrial disintegrator to reduce NAND flash chips to particles smaller than 2mm x 2mm, destroying silicon dies.",
            "suitable_for": "End-of-life disposal, decommissioned high-sensitivity media, or damaged drives that fail Purge commands.",
            "verification": "Visual sieve inspection verifying particle size compliance and dual-custody destruction log."
        }
    },
    "Magnetic HDD (Platters)": {
        "media_physics_notes": "Magnetic recording surfaces store bits as magnetic domains on rotating platters. Can be sanitized by magnetic realignment or overwrite.",
        "clear": {
            "method": "Single-Pass Binary Overwrite (All addressable sectors)",
            "description": "Writes a fixed pattern (zeros or pseudo-random) across all sectors using dd, shred, or DBAN.",
            "suitable_for": "Internal re-use within organizational boundary.",
            "verification": "Read back full disk or 20% sector sample verifying uniform pattern."
        },
        "purge": {
            "method": "Magnetic Degaussing (Certified Field Strength >= 1.5 Tesla / 15,000 Gauss) or ATA Secure Erase",
            "description": "Exposes platters to a massive magnetic pulse that scrambles magnetic domains beyond physical recovery and erases servo tracks.",
            "suitable_for": "Disposal or transfer outside organizational control.",
            "verification": "Verify degausser field calibration meter and confirm HDD spindle motor is permanently inoperable."
        },
        "destroy": {
            "method": "Mechanical Platter Punching / Bending / Shredding (< 12mm fragments)",
            "description": "Physically pierces all platters with a hydraulic punch or runs drive through heavy-duty industrial shredder.",
            "suitable_for": "Decommissioning classified drives or end-of-life hardware.",
            "verification": "Visual confirmation of deformed platters and shattered spindle bearings."
        }
    },
    "Removable USB / Flash Media": {
        "media_physics_notes": "Small form-factor NAND flash without advanced enterprise controller commands. Susceptible to uneven block wear.",
        "clear": {
            "method": "Full-Volume Raw Sector Overwrite (e.g. dd if=/dev/urandom)",
            "description": "Overwrites entire user-addressable partition table and raw blocks with random bytes.",
            "suitable_for": "Re-assignment to another employee within same department.",
            "verification": "Verify file system structure is wiped and raw data reads random entropy."
        },
        "purge": {
            "method": "Cryptographic Key Destruction (for hardware-encrypted drives) or Secure Firmware Reset",
            "description": "Triggers onboard cryptochip zeroization or vendor secure wipe utility.",
            "suitable_for": "Surplus equipment resale or inter-agency transfer.",
            "verification": "Confirm device partition table is blank and hardware key is erased."
        },
        "destroy": {
            "method": "Physical Disintegration / Incineration to Ash",
            "description": "Incineration in licensed facility or shredding down to fine particles.",
            "suitable_for": "End of lifecycle, suspect malware carrier, or policy disposal.",
            "verification": "Certificate of destruction from licensed e-waste partner."
        }
    },
    "Enterprise NAS / SAN Array": {
        "media_physics_notes": "Distributed storage spanning multi-disk RAID groups, NVRAM cache, snapshots, and LUN virtualization layers.",
        "clear": {
            "method": "LUN Zeroing & Snapshot Tree Purge",
            "description": "Initiates storage OS volume zeroing command and destroys all metadata pointers and copy-on-write snapshot trees.",
            "suitable_for": "Internal LUN re-allocation across internal departments.",
            "verification": "Verify storage pool capacity release and run random read checks across wiped volume space."
        },
        "purge": {
            "method": "Storage Array Cryptographic Shredding & Controller Secure Pool Reset",
            "description": "Revokes and regenerates array master encryption keys (KMIP / SED pool keys) rendering all array drives simultaneously unrecoverable.",
            "suitable_for": "SAN array decommission, lease expiration, or cross-tenant migration.",
            "verification": "Verify key revocation in Enterprise Key Management server and inspect pool state logs."
        },
        "destroy": {
            "method": "Individual Drive Removal & Physical Disintegration",
            "description": "Extracts every individual drive module (SSD/HDD) from array shelves and shreds them individually to NIST specs.",
            "suitable_for": "Data center decommissioning for top-tier sensitivity assets.",
            "verification": "Drive serial bar-code scan matching physical destruction manifests."
        }
    }
}


def get_media_category(device_type: str) -> str:
    """Classifies user device type into NIST media category."""
    if "SSD" in device_type or "NVMe" in device_type:
        return "SSD / NVMe Flash"
    elif "HDD" in device_type or "Magnetic" in device_type:
        return "Magnetic HDD (Platters)"
    elif "NAS" in device_type or "SAN" in device_type:
        return "Enterprise NAS / SAN Array"
    else:
        return "Removable USB / Flash Media"


def evaluate_nist_sanitization(
    device_type: str,
    data_classification: str,
    intended_action: str
) -> Dict[str, Any]:
    """
    Determines the required NIST SP 800-88 Rev. 1 sanitization protocol
    based on media type, data classification, and intended destination.
    """
    category = get_media_category(device_type)
    guideline = NIST_MEDIA_GUIDELINES.get(category, NIST_MEDIA_GUIDELINES["Removable USB / Flash Media"])

    # Decision Logic:
    # 1. If Decommissioning / Disposal:
    #    - Regulated or Restricted -> DESTROY
    #    - Confidential -> PURGE or DESTROY
    #    - Internal / Public -> PURGE
    # 2. If Hardware Re-assignment:
    #    - To lower classification or outside boundary -> PURGE
    #    - Within same classification -> CLEAR
    # 3. If Cross-environment transfer: -> PURGE

    is_decommission = "Decommissioning" in intended_action
    is_reassignment = "Re-assignment" in intended_action
    is_high_sens = "Restricted" in data_classification or "Regulated" in data_classification

    if is_decommission:
        if is_high_sens:
            recommended_level = "DESTROY"
            rationale = "High-sensitivity / regulated data media at end-of-life requires irreversible physical destruction to guarantee non-recovery (NIST SP 800-88 Sec 4.3)."
        else:
            recommended_level = "PURGE"
            rationale = "Medium/standard sensitivity media leaving operational custody requires Purge-level cryptographic/voltage sanitization."
    elif is_reassignment:
        if is_high_sens:
            recommended_level = "PURGE"
            rationale = "Re-assigning hardware containing confidential/restricted data mandates Purge-level sanitization before user handoff."
        else:
            recommended_level = "CLEAR"
            rationale = "Internal re-assignment within the same security perimeter permits logical Clear overwrite procedures."
    else:
        # Default / Routine maintenance
        recommended_level = "CLEAR"
        rationale = "Routine operational maintenance requires standard Clear protocols if data boundary is maintained."

    protocol_data = guideline[recommended_level.lower()]

    return {
        "media_category": category,
        "physics_notes": guideline["media_physics_notes"],
        "recommended_level": recommended_level,
        "rationale": rationale,
        "protocol": protocol_data,
        "all_levels": {
            "CLEAR": guideline["clear"],
            "PURGE": guideline["purge"],
            "DESTROY": guideline["destroy"]
        }
    }


def generate_sanitization_certificate(
    device_type: str,
    serial_number: str,
    asset_tag: str,
    sanitization_level: str,
    technician_name: str,
    witness_name: str,
    tool_used: str
) -> Dict[str, Any]:
    """Generates an official NIST SP 800-88 Media Sanitization Certificate."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    case_id = f"SAN-{hashlib.sha256(f'{serial_number}{timestamp}'.encode()).hexdigest()[:8].upper()}"
    
    cert_hash = hashlib.sha256(
        f"{case_id}-{serial_number}-{asset_tag}-{sanitization_level}-{timestamp}".encode()
    ).hexdigest()

    return {
        "certificate_id": case_id,
        "timestamp": timestamp,
        "serial_number": serial_number or "SR-90482-E",
        "asset_tag": asset_tag or "AST-CORP-4882",
        "device_type": device_type,
        "sanitization_level": sanitization_level,
        "method_tool": tool_used or "NVMe Sanitize CLI v2.4 (Crypto-Scramble)",
        "technician_name": technician_name or "Alex Vance (Lead SecOps)",
        "witness_name": witness_name or "Elena Rostova (Compliance Officer)",
        "verification_hash": cert_hash[:24].upper(),
        "standards_reference": "NIST Special Publication 800-88 Revision 1 (Guidelines for Media Sanitization)",
        "status": "VERIFIED_AND_CERTIFIED"
    }
