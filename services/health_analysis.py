# ─────────────────────────────────────────────────────────────────
# services/health_analysis.py — Vital sign analysis
# ─────────────────────────────────────────────────────────────────

from config import TEMP_HIGH, TEMP_LOW, HR_LOW, HR_HIGH
from utils.logger import get_logger

log = get_logger("services.health")


def analyze_vitals(temperature, heart_rate):
    """
    Analyzes vital signs and returns status for each parameter.

    Returns: dict with keys:
        temp_status  : "normal" | "warning" | "critical"
        hr_status    : "normal" | "warning" | "critical"
        temp_message : str
        hr_message   : str
        is_critical  : bool
    """
    result = {
        "temp_status" : "normal",
        "hr_status"   : "normal",
        "temp_message": "Normal range",
        "hr_message"  : "Normal range",
        "is_critical" : False,
    }

    # ── Temperature Analysis ──────────────────────────────────────
    if temperature is not None:
        if temperature > TEMP_HIGH:
            result["temp_status"]  = "critical"
            result["temp_message"] = f"High fever ({temperature}°C)"
            result["is_critical"]  = True
        elif temperature > 37.5:
            result["temp_status"]  = "warning"
            result["temp_message"] = f"Mild fever ({temperature}°C)"
        elif temperature < TEMP_LOW:
            result["temp_status"]  = "critical"
            result["temp_message"] = f"Hypothermia ({temperature}°C)"
            result["is_critical"]  = True
        else:
            result["temp_message"] = f"Normal ({temperature}°C)"

    # ── Heart Rate Analysis ───────────────────────────────────────
    if heart_rate is not None:
        if heart_rate < HR_LOW:
            result["hr_status"]  = "critical"
            result["hr_message"] = f"Bradycardia ({heart_rate} BPM)"
            result["is_critical"] = True
        elif heart_rate > HR_HIGH:
            result["hr_status"]  = "critical"
            result["hr_message"] = f"Tachycardia ({heart_rate} BPM)"
            result["is_critical"] = True
        elif heart_rate > 100:
            result["hr_status"]  = "warning"
            result["hr_message"] = f"Elevated ({heart_rate} BPM)"
        else:
            result["hr_message"] = f"Normal ({heart_rate} BPM)"

    return result


def get_health_summary(session):
    """
    Generates a text summary of patient health for display.
    """
    temp = session.get("temperature")
    hr   = session.get("heart_rate")
    env  = session.get("env", {})

    analysis = analyze_vitals(temp, hr)

    lines = []
    lines.append(f"Body Temperature: {temp}°C — {analysis['temp_message']}")
    lines.append(f"Heart Rate: {hr} BPM — {analysis['hr_message']}")

    if env.get("amb_temp"):
        lines.append(
            f"Environment: {env['amb_temp']}°C, "
            f"{env['humidity']}% humidity, "
            f"{env['pressure']} hPa"
        )

    if analysis["is_critical"]:
        lines.append("")
        lines.append("⚠ CRITICAL VALUES DETECTED")

    return "\n".join(lines)
