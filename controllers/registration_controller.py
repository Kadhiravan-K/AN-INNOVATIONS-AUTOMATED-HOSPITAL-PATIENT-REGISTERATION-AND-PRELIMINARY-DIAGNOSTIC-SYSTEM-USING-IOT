# ─────────────────────────────────────────────────────────────────
# controllers/registration_controller.py — Session & flow manager
# ─────────────────────────────────────────────────────────────────

from database.db_operations import save_full_registration
from services.ai_diagnostic import ai_diagnostic
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

    def save_patient_info(self, name, age, gender, visit_type, allergies="", history=""):
        """Save patient personal and clinical information to session."""
        self.session["name"]            = name
        self.session["age"]             = int(age)
        self.session["gender"]          = gender
        self.session["visit_type"]      = visit_type
        self.session["allergies"]       = allergies
        self.session["medical_history"] = history

    def save_aadhaar(self, aadhaar_number):
        """Store aadhaar number in session."""
        self.session["aadhaar_number"] = aadhaar_number

    def update_demographics(self, demographics):
        """Merge demographics and fetch previous history if available."""
        self.session.update(demographics)
        
        # Check for previous history
        from database.db_operations import get_previous_visit_by_aadhaar
        if self.session.get("aadhaar_number"):
            prev = get_previous_visit_by_aadhaar(self.session["aadhaar_number"])
            if prev:
                self.session["previous_visit"] = prev
                self.session["allergies"]       = prev.get("allergies", "")
                self.session["medical_history"] = prev.get("medical_history", "")
                log.info("Previous history loaded for patient.")

    def save_symptoms(self, symptom_codes):
        """Save selected symptom codes to session."""
        self.session["symptoms"] = symptom_codes

    def save_health_data(self, temperature, heart_rate, env, spo2=None):
        """Save sensor readings to session."""
        self.session["temperature"] = temperature
        self.session["heart_rate"]  = heart_rate
        self.session["env"]         = env
        self.session["spo2"]        = spo2

    def perform_triage(self):
        """Run department allocation based on AI analysis of symptoms and vitals."""
        dept, doctor, severity, is_emg = ai_diagnostic.analyze(
            self.session.get("symptoms", []),
            self.session.get("temperature"),
            self.session.get("heart_rate"),
            self.session.get("spo2"),
        )
        self.session["department"]   = dept
        self.session["doctor_type"]  = doctor
        self.session["severity"]     = severity
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
