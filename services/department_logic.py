# ─────────────────────────────────────────────────────────────────
# services/department_logic.py — Triage & Department Allocation
# ─────────────────────────────────────────────────────────────────

from config import SYMPTOM_DEPT_MAP, TEMP_HIGH, HR_LOW, HR_HIGH
from utils.logger import get_logger

log = get_logger("services.dept")


def allocate_department(symptoms, temperature, heart_rate):
    """
    Determines the appropriate medical department based on:
    - Selected symptoms
    - Measured body temperature
    - Measured heart rate

    Returns: tuple (department: str, doctor_type: str, is_emergency: bool)
    """
    # ── Critical Alert Check (Emergency) ─────────────────────────
    is_emergency = False
    if temperature and (temperature > TEMP_HIGH):
        is_emergency = True
    if heart_rate and (heart_rate < HR_LOW or heart_rate > HR_HIGH):
        is_emergency = True

    if is_emergency:
        log.warning("EMERGENCY detected! Temp=%.1f, HR=%s",
                     temperature or 0, heart_rate or 0)
        return "Emergency", "Emergency Physician", True

    # ── Symptom-Based Scoring ─────────────────────────────────────
    scores = {}
    for symptom in symptoms:
        dept = SYMPTOM_DEPT_MAP.get(symptom, "General Medicine")
        scores[dept] = scores.get(dept, 0) + 1

    if not scores:
        return "General Medicine", "General Practitioner", False

    # Department with highest symptom score wins
    best_dept   = max(scores, key=scores.get)
    doctor_type = (
        "General Practitioner"
        if best_dept == "General Medicine"
        else "Specialist"
    )

    log.info("Allocated: %s → %s", best_dept, doctor_type)
    return best_dept, doctor_type, False
