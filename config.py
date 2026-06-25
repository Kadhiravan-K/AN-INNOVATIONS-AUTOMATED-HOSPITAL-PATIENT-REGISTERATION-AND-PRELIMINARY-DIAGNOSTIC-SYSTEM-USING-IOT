# ─────────────────────────────────────────────────────────────────
# config.py
# Project  : Automated Hospital Patient Registration System
# College  : Hindusthan College of Engineering and Technology
# Dept     : Electrical and Electronics Engineering
# Guide    : Dr. R. Rajeshkanna
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

# ── COLOUR THEME ─────────────────────────────────────────────────
COLOR_DARK    = "#1F4E79"   # Dark blue  – header background
COLOR_BLUE    = "#2E75B6"   # Medium blue – buttons
COLOR_LIGHT   = "#EBF5FB"   # Light blue – card background
COLOR_WHITE   = "#FFFFFF"   # White      – main background
COLOR_RED     = "#C0392B"   # Red        – emergency / error
COLOR_GREEN   = "#1E8449"   # Green      – success

# ── FONTS ────────────────────────────────────────────────────────
FONT_TITLE    = ("Arial", 18, "bold")
FONT_HEADING  = ("Arial", 14, "bold")
FONT_NORMAL   = ("Arial", 12)
FONT_SMALL    = ("Arial", 10)
FONT_CODE     = ("Courier New", 11)

# ── SENSOR THRESHOLDS (for emergency alert) ──────────────────────
TEMP_HIGH     = 38.5   # °C  – high grade fever threshold
HR_LOW        = 50     # BPM – bradycardia threshold
HR_HIGH       = 120    # BPM – tachycardia threshold

# ── HOSPITAL INFO (shown on token) ───────────────────────────────
HOSPITAL_NAME = "Hindusthan College of Engineering and Technology"
HOSPITAL_CITY = "Coimbatore – 641 032"

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
    "fever"               : "Fever",
    "chest_pain"          : "Chest Pain",
    "shortness_of_breath" : "Shortness of Breath",
    "headache"            : "Headache",
    "abdominal_pain"      : "Abdominal Pain",
    "joint_pain"          : "Joint Pain",
    "ear_pain"            : "Ear Pain",
    "eye_problem"         : "Eye Problem",
    "skin_rash"           : "Skin Rash",
    "urinary_problem"     : "Urinary Problem",
    "dental_pain"         : "Dental Pain",
    "anxiety_depression"  : "Anxiety / Depression",
}