# ─────────────────────────────────────────────────────────────────
# database/models.py — Data classes for structured records
# ─────────────────────────────────────────────────────────────────

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Patient:
    """Represents a registered patient."""
    patient_id: Optional[int] = None
    name: str = ""
    age: int = 0
    gender: str = ""
    aadhaar_hash: Optional[str] = None
    registration_type: str = "Temporary"
    created_at: str = ""


@dataclass
class HealthRecord:
    """Represents a single health measurement record."""
    record_id: Optional[int] = None
    patient_id: int = 0
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    amb_temp: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    recorded_at: str = ""


@dataclass
class SymptomRecord:
    """Represents a selected symptom entry."""
    symptom_id: Optional[int] = None
    patient_id: int = 0
    symptom_code: str = ""
    recorded_at: str = ""


@dataclass
class Token:
    """Represents a registration token."""
    token_id: Optional[int] = None
    patient_id: int = 0
    token_number: str = ""
    department: str = ""
    doctor_type: str = ""
    is_emergency: bool = False
    status: str = "waiting"
    issued_at: str = ""


@dataclass
class PatientSummary:
    """Complete patient summary for display on token screen."""
    name: str = "Unknown"
    age: int = 0
    gender: str = "--"
    registration_type: str = "--"
    registered_at: str = "--"
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    amb_temp: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    token_number: str = "--"
    department: str = "--"
    doctor_type: str = "--"
    is_emergency: bool = False
    issued_at: str = "--"
    symptoms: List[str] = field(default_factory=list)
