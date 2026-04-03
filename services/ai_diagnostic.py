# ─────────────────────────────────────────────────────────────────
# services/ai_diagnostic.py — Weighted Scoring & Severity Prediction
# ─────────────────────────────────────────────────────────────────

from config import (
    SYMPTOM_DEPT_MAP, TEMP_HIGH, TEMP_LOW, HR_LOW, HR_HIGH
)
from utils.logger import get_logger

log = get_logger("services.ai")

class AIDiagnostic:
    """
    Advanced diagnostic logic using weighted scoring and severity ranking.
    This simulates an ML model by considering dependencies between symptoms and vitals.
    """

    # Weights for risk factors (0.0 to 1.0)
    RISK_WEIGHTS = {
        "chest_pain": 0.9,
        "shortness_of_breath": 0.8,
        "fever": 0.3,
        "headache": 0.2,
        "anxiety": 0.1,
    }

    # Mapping of departments to specific doctor names
    DEPARTMENT_DOCTORS = {
        "General Medicine": "Dr. Aarav Sharma",
        "Cardiology": "Dr. Priya Iyer",
        "Pulmonology": "Dr. Vikram Singh",
        "Neurology": "Dr. Ananya Reddy",
        "Gastroenterology": "Dr. Rohan Gupta",
        "Orthopaedics": "Dr. Meera Das",
        "ENT": "Dr. Sameer Khan",
        "Ophthalmology": "Dr. Kavita Nair",
        "Dermatology": "Dr. Arjun Verma",
        "Urology": "Dr. Sanjay Bose",
        "Dental": "Dr. Neha Kapoor",
        "Psychiatry": "Dr. Aditya Joshi",
        "Emergency": "Dr. Rajesh Kumar (On-Call)"
    }

    def __init__(self):
        pass

    def analyze(self, symptoms, temperature, heart_rate, spo2=None):
        """
        Main analysis pipeline.
        Returns: tuple (department: str, doctor: str, severity: str, is_emergency: bool)
        """
        severity_score = 0.0
        
        # 1. Calculate base severity from symptoms
        for s in symptoms:
            severity_score += self.RISK_WEIGHTS.get(s, 0.1)

        # 2. Factor in Vitals (Vitals are heavy multipliers)
        if temperature and temperature > TEMP_HIGH:
            severity_score *= 1.5
        if heart_rate and (heart_rate < HR_LOW or heart_rate > HR_HIGH):
            severity_score *= 2.0
        if spo2 and spo2 < 92:
            severity_score *= 2.5  # Critical respiratory risk

        # 3. Determine Urgency
        is_emergency = severity_score > 1.5
        severity = "Critical" if severity_score > 1.2 else "High" if severity_score > 0.7 else "Normal"

        if is_emergency:
            log.warning(f"AI ALERT: Emergency detected! Score: {severity_score:.2f}")
            doctor = self.DEPARTMENT_DOCTORS.get("Emergency", "Duty Physician")
            return "Emergency", doctor, severity, True

        # 4. Smart Department Allocation
        # (Weighted voting based on symptoms)
        dept_votes = {}
        for s in symptoms:
            dept = SYMPTOM_DEPT_MAP.get(s, "General Medicine")
            weight = self.RISK_WEIGHTS.get(s, 0.2)
            dept_votes[dept] = dept_votes.get(dept, 0) + weight

        if not dept_votes:
            doctor = self.DEPARTMENT_DOCTORS.get("General Medicine", "General Physician")
            return "General Medicine", doctor, severity, False

        best_dept = max(dept_votes, key=dept_votes.get)
        doctor = self.DEPARTMENT_DOCTORS.get(best_dept, "Specialist")

        log.info(f"AI Inference: {best_dept} ({severity})")
        return best_dept, doctor, severity, False

# Global instance
ai_diagnostic = AIDiagnostic()
