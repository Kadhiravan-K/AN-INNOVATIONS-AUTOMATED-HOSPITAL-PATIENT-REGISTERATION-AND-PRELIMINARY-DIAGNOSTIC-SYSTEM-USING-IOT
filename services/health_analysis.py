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
        "spo2_status" : "normal",
        "temp_message": "Normal range",
        "hr_message"  : "Normal range",
        "spo2_message": "Normal",
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

    # ── SpO2 Analysis ──────────────────────────────────────────────
    def analyze_spo2(spo2):
        if spo2 is None: return "normal", "N/A"
        if spo2 < 92: return "critical", f"Low Oxygen ({spo2}%)"
        if spo2 < 95: return "warning", f"Mild Hypoxia ({spo2}%)"
        return "normal", f"Normal ({spo2}%)"

    # We hackishly update the result since this is a refactor
    # (In a real app, I'd pass spo2 to analyze_vitals properly)
    return result

def analyze_vitals_full(temperature, heart_rate, spo2=None):
    """Refactored version to handle all vitals."""
    res = analyze_vitals(temperature, heart_rate)
    res["spo2_status"] = "normal"
    res["spo2_message"] = "Normal"
    
    if spo2 is not None:
        if spo2 < 92:
            res["spo2_status"] = "critical"
            res["spo2_message"] = f"Low Oxygen ({spo2}%)"
            res["is_critical"] = True
        elif spo2 < 95:
            res["spo2_status"] = "warning"
            res["spo2_message"] = f"Mild Hypoxia ({spo2}%)"
        else:
            res["spo2_message"] = f"Normal ({spo2}%)"
    
    return res


def get_health_summary(session):
    """
    Generates a text summary of patient health for display.
    """
    temp = session.get("temperature")
    hr   = session.get("heart_rate")
    spo2 = session.get("spo2")
    env  = session.get("env", {})

    analysis = analyze_vitals_full(temp, hr, spo2)

    lines = []
    lines.append(f"Body Temperature: {temp}°C — {analysis['temp_message']}")
    lines.append(f"Heart Rate: {hr} BPM — {analysis['hr_message']}")
    lines.append(f"Oxygen (SpO2): {spo2}% — {analysis['spo2_message']}")

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
