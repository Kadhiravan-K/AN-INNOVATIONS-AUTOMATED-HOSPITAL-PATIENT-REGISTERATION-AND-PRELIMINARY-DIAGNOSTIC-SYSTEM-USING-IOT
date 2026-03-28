# ─────────────────────────────────────────────────────────────────
# config.py
# Project  : Automated Hospital Patient Registration System
# ─────────────────────────────────────────────────────────────────

# ── MOCK MODE ────────────────────────────────────────────────────
# Set True  → runs on your Laptop (no hardware needed)
# Set False → runs on real Raspberry Pi with sensors
MOCK_MODE = True

# ── GPIO PIN NUMBERS (Raspberry Pi BCM mode) ─────────────────────
BUZZER_PIN = 27       # Active buzzer
TOUCH_PIN  = 18       # TTP223 capacitive touch sensor
PULSE_PIN  = 17       # KY-039 pulse sensor (via comparator)

# ── I2C SENSOR ADDRESSES ─────────────────────────────────────────
MLX90614_ADDR = 0x5A  # IR Temperature sensor
BME280_ADDR   = 0x76  # Environmental sensor

# ── DATABASE ─────────────────────────────────────────────────────
DB_PATH = "hospital_kiosk.db"   # SQLite database file name

# ── GUI SETTINGS ─────────────────────────────────────────────────
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 480
FULLSCREEN    = False  # Set True on actual Raspberry Pi kiosk

# ── MODERN COLOUR PALETTE ────────────────────────────────────────
COLOR_PRIMARY    = "#0D1B2A"   # Deep navy      – headers, accents
COLOR_SECONDARY  = "#1B3A4B"   # Dark steel     – secondary bg
COLOR_ACCENT     = "#1B998B"   # Teal           – buttons, highlights
COLOR_SURFACE    = "#F8F9FA"   # Warm white     – main background
COLOR_CARD       = "#FFFFFF"   # Pure white     – cards
COLOR_TEXT       = "#212529"   # Near black     – primary text
COLOR_TEXT_LIGHT = "#6C757D"   # Grey           – secondary text
COLOR_SUCCESS    = "#2DC653"   # Green          – success states
COLOR_WARNING    = "#F77F00"   # Amber          – warning states
COLOR_DANGER     = "#D62828"   # Red            – emergency / error
COLOR_INFO       = "#457B9D"   # Steel blue     – informational
COLOR_BORDER     = "#DEE2E6"   # Light grey     – borders, dividers

# Legacy aliases (for backward compatibility during migration)
COLOR_DARK    = COLOR_PRIMARY
COLOR_BLUE    = COLOR_ACCENT
COLOR_LIGHT   = "#E8F4F8"
COLOR_WHITE   = COLOR_SURFACE
COLOR_RED     = COLOR_DANGER
COLOR_GREEN   = COLOR_SUCCESS

# ── FONTS ────────────────────────────────────────────────────────
FONT_TITLE    = ("Segoe UI", 20, "bold")
FONT_HEADING  = ("Segoe UI", 14, "bold")
FONT_NORMAL   = ("Segoe UI", 12)
FONT_SMALL    = ("Segoe UI", 10)
FONT_TINY     = ("Segoe UI", 9)
FONT_CODE     = ("Consolas", 11)
FONT_LARGE    = ("Segoe UI", 28, "bold")
FONT_ICON     = ("Segoe UI", 24)

# ── ANIMATION TIMING ─────────────────────────────────────────────
ANIM_FADE_MS      = 15    # ms between fade steps
ANIM_FADE_STEPS   = 12    # number of fade steps
ANIM_SLIDE_MS     = 8     # ms between slide steps
ANIM_PULSE_MS     = 800   # ms for pulse/blink cycle
ANIM_PROGRESS_MS  = 50    # ms between progress bar updates
SCREEN_TIMEOUT_MS = 120000  # 2 minutes auto-reset

# ── SENSOR THRESHOLDS (for emergency alert) ──────────────────────
TEMP_HIGH     = 38.5   # °C  – high grade fever threshold
TEMP_LOW      = 35.0   # °C  – hypothermia threshold
HR_LOW        = 50     # BPM – bradycardia threshold
HR_HIGH       = 120    # BPM – tachycardia threshold

# ── HOSPITAL INFO (shown on token) ───────────────────────────────
HOSPITAL_NAME = "AN Innovations Hospital"
HOSPITAL_CITY = "Smart Healthcare Kiosk"

# ── DEPARTMENT SYMPTOM MAPPING ───────────────────────────────────
SYMPTOM_DEPT_MAP = {
    "fever"               : "General Medicine",
    "chest_pain"          : "Cardiology",
    "shortness_of_breath" : "Pulmonology",
    "headache"            : "Neurology",
    "abdominal_pain"      : "Gastroenterology",
    "joint_pain"          : "Orthopaedics",
    "ear_pain"            : "ENT",
    "eye_problem"         : "Ophthalmology",
    "skin_rash"           : "Dermatology",
    "urinary_problem"     : "Urology",
    "dental_pain"         : "Dental",
    "anxiety_depression"  : "Psychiatry",
}

# ── SYMPTOM DISPLAY LABELS ───────────────────────────────────────
SYMPTOM_LABELS = {
    "fever"               : "🌡  Fever",
    "chest_pain"          : "💔  Chest Pain",
    "shortness_of_breath" : "😮‍💨  Shortness of Breath",
    "headache"            : "🤕  Headache",
    "abdominal_pain"      : "🤢  Abdominal Pain",
    "joint_pain"          : "🦴  Joint Pain",
    "ear_pain"            : "👂  Ear Pain",
    "eye_problem"         : "👁  Eye Problem",
    "skin_rash"           : "🔴  Skin Rash",
    "urinary_problem"     : "💧  Urinary Problem",
    "dental_pain"         : "🦷  Dental Pain",
    "anxiety_depression"  : "🧠  Anxiety / Depression",
}

# ── SYMPTOM CATEGORIES (for grouped display) ─────────────────────
SYMPTOM_CATEGORIES = {
    "General": ["fever", "headache"],
    "Heart & Lungs": ["chest_pain", "shortness_of_breath"],
    "Digestive": ["abdominal_pain"],
    "Bones & Joints": ["joint_pain"],
    "ENT & Eyes": ["ear_pain", "eye_problem"],
    "Skin & Other": ["skin_rash", "urinary_problem", "dental_pain", "anxiety_depression"],
}

# ── LOGGING ──────────────────────────────────────────────────────
LOG_FILE   = "hospital_kiosk.log"
LOG_LEVEL  = "INFO"