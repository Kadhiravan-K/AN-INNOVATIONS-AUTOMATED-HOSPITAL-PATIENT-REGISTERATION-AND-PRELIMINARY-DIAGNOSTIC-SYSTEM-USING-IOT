# ─────────────────────────────────────────────────────────────────
# utils/report_generator.py — Token / receipt printing
# ─────────────────────────────────────────────────────────────────

import datetime
from config import HOSPITAL_NAME, HOSPITAL_CITY
from utils.logger import get_logger

log = get_logger("report")


def generate_print_report(session):
    """
    Formats and prints a patient token / receipt to console.
    For thermal printer: replace print() with ESC/POS commands.

    Parameters:
        session : dict — full session data

    Returns:
        str — the formatted report text
    """
    now = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")

    lines = [
        "",
        "=" * 48,
        f"  {HOSPITAL_NAME}",
        f"  {HOSPITAL_CITY}",
        "=" * 48,
        f"  TOKEN        : {session.get('token_number', '--')}",
        f"  NAME         : {session.get('name', '--')}",
        f"  AGE / GENDER : {session.get('age', '--')} / "
        f"{session.get('gender', '--')}",
        f"  DEPARTMENT   : {session.get('department', '--')}",
        f"  DOCTOR       : {session.get('doctor_type', '--')}",
        f"  TEMPERATURE  : {session.get('temperature', '--')} °C",
        f"  HEART RATE   : {session.get('heart_rate', '--')} BPM",
        f"  VISIT TYPE   : {session.get('visit_type', '--')}",
        f"  DATE & TIME  : {now}",
        "-" * 48,
    ]

    # Add symptoms if present
    symptoms = session.get("symptoms", [])
    if symptoms:
        from config import SYMPTOM_LABELS
        symptom_names = [SYMPTOM_LABELS.get(s, s) for s in symptoms]
        lines.append(f"  SYMPTOMS     : {', '.join(symptom_names)}")

    # Emergency flag
    if session.get("is_emergency"):
        lines.append("")
        lines.append("  ⚠  CRITICAL VALUES – EMERGENCY DEPARTMENT")

    lines.append("=" * 48)
    lines.append("")

    report = "\n".join(lines)

    # Print to console (replace with thermal printer in production)
    print(report)
    log.info("Token report printed for patient: %s", session.get("name", "Unknown"))

    return report
