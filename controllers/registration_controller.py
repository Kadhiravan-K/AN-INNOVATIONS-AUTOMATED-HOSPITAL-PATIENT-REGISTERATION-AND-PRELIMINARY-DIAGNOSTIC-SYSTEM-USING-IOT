# ─────────────────────────────────────────────────────────────────
# controllers/registration_controller.py — Session & flow manager
# ─────────────────────────────────────────────────────────────────

from database.db_operations import save_full_registration
from services.department_logic import allocate_department
from auth.aadhaar_auth import reset_auth
from utils.logger import get_logger

log = get_logger("controller.reg")


class RegistrationController:
    """Manages session state and orchestrates the registration flow."""

    def __init__(self):
        self.session = {}

    def start_session(self):
        """Reset session for a new patient."""
        self.session = {}
        reset_auth()
        log.info("New registration session started.")

    def set_registration_type(self, reg_type):
        """Set registration type: 'Permanent' or 'Temporary'."""
        self.session["registration_type"] = reg_type

    def save_patient_info(self, name, age, gender, visit_type):
        """Save patient personal information to session."""
        self.session["name"]       = name
        self.session["age"]        = int(age)
        self.session["gender"]     = gender
        self.session["visit_type"] = visit_type

    def save_aadhaar(self, aadhaar_number):
        """Store aadhaar number in session."""
        self.session["aadhaar_number"] = aadhaar_number

    def update_demographics(self, demographics):
        """Merge demographics from Aadhaar verification into session."""
        self.session.update(demographics)

    def save_symptoms(self, symptom_codes):
        """Save selected symptom codes to session."""
        self.session["symptoms"] = symptom_codes

    def save_health_data(self, temperature, heart_rate, env):
        """Save sensor readings to session."""
        self.session["temperature"] = temperature
        self.session["heart_rate"]  = heart_rate
        self.session["env"]         = env

    def perform_triage(self):
        """Run department allocation based on symptoms and vitals."""
        dept, doctor, is_emg = allocate_department(
            self.session.get("symptoms", []),
            self.session.get("temperature"),
            self.session.get("heart_rate"),
        )
        self.session["department"]   = dept
        self.session["doctor_type"]  = doctor
        self.session["is_emergency"] = is_emg
        return dept, doctor, is_emg

    def complete_registration(self):
        """Save everything to database and return result."""
        result = save_full_registration(self.session)
        self.session["token_number"] = result["token_number"]
        self.session["patient_id"]   = result["patient_id"]
        log.info("Registration complete. Token: %s", result["token_number"])
        return result

    def get_session(self):
        """Return a copy of the current session data."""
        return dict(self.session)
