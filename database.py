# ─────────────────────────────────────────────────────────────────
# database.py
# Project  : Automated Hospital Patient Registration System
# College  : Hindusthan College of Engineering and Technology
# Dept     : Electrical and Electronics Engineering
# Guide    : Dr. R. Rajeshkanna
# ─────────────────────────────────────────────────────────────────

import sqlite3
import hashlib
import datetime
import random
from config import DB_PATH


# ─────────────────────────────────────────────────────────────────
# DATABASE SETUP – Create tables if not exist
# ─────────────────────────────────────────────────────────────────

def init_database():
    """
    Creates all required tables in the SQLite database.
    Safe to call multiple times – uses CREATE IF NOT EXISTS.
    Call this once when the app starts.
    """
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()

    # ── Table 1: patients ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT,
            age               INTEGER,
            gender            TEXT,
            aadhaar_hash      TEXT,
            registration_type TEXT,
            created_at        TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── Table 2: health_records ───────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS health_records (
            record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id   INTEGER,
            temperature  REAL,
            heart_rate   INTEGER,
            amb_temp     REAL,
            humidity     REAL,
            pressure     REAL,
            recorded_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

    # ── Table 3: symptoms ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS symptoms (
            symptom_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id   INTEGER,
            symptom_code TEXT,
            recorded_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

    # ── Table 4: tokens ───────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            token_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id   INTEGER,
            token_number TEXT,
            department   TEXT,
            doctor_type  TEXT,
            is_emergency INTEGER DEFAULT 0,
            status       TEXT    DEFAULT "waiting",
            issued_at    TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("[DB] Database initialised successfully.")


# ─────────────────────────────────────────────────────────────────
# TOKEN GENERATOR
# ─────────────────────────────────────────────────────────────────

def generate_token_number():
    """
    Generates a unique token number.
    Format: YYYYMMDD-XXXX  (e.g. 20260328-4721)
    Returns: str
    """
    date_part   = datetime.datetime.now().strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"{date_part}-{random_part}"


# ─────────────────────────────────────────────────────────────────
# SAVE PATIENT RECORD
# ─────────────────────────────────────────────────────────────────

def save_patient(name, age, gender, aadhaar_number, registration_type):
    """
    Saves a new patient record to the database.
    Aadhaar number is stored as SHA-256 hash for privacy.

    Returns: int – newly created patient_id
    """
    # Hash Aadhaar number – never store plain text
    aadhaar_hash = (
        hashlib.sha256(aadhaar_number.encode()).hexdigest()
        if aadhaar_number
        else None
    )

    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO patients (name, age, gender, aadhaar_hash, registration_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, gender, aadhaar_hash, registration_type))

    patient_id = c.lastrowid
    conn.commit()
    conn.close()

    print(f"[DB] Patient saved. ID: {patient_id}")
    return patient_id


# ─────────────────────────────────────────────────────────────────
# SAVE HEALTH RECORD
# ─────────────────────────────────────────────────────────────────

def save_health_record(patient_id, temperature, heart_rate, env):
    """
    Saves sensor readings linked to a patient.

    Parameters:
        patient_id  : int
        temperature : float  – body temperature °C
        heart_rate  : int    – BPM
        env         : dict   – {amb_temp, humidity, pressure}
    """
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO health_records
            (patient_id, temperature, heart_rate, amb_temp, humidity, pressure)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        patient_id,
        temperature,
        heart_rate,
        env.get("amb_temp"),
        env.get("humidity"),
        env.get("pressure"),
    ))
    conn.commit()
    conn.close()
    print(f"[DB] Health record saved for patient ID: {patient_id}")


# ─────────────────────────────────────────────────────────────────
# SAVE SYMPTOMS
# ─────────────────────────────────────────────────────────────────

def save_symptoms(patient_id, symptoms):
    """
    Saves all selected symptom codes for a patient.

    Parameters:
        patient_id : int
        symptoms   : list of str  – e.g. ['fever', 'headache']
    """
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    for symptom in symptoms:
        c.execute('''
            INSERT INTO symptoms (patient_id, symptom_code)
            VALUES (?, ?)
        ''', (patient_id, symptom))
    conn.commit()
    conn.close()
    print(f"[DB] {len(symptoms)} symptom(s) saved for patient ID: {patient_id}")


# ─────────────────────────────────────────────────────────────────
# SAVE TOKEN
# ─────────────────────────────────────────────────────────────────

def save_token(patient_id, department, doctor_type, is_emergency):
    """
    Generates and saves a registration token for a patient.

    Returns: str – the generated token number
    """
    token_number = generate_token_number()

    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO tokens
            (patient_id, token_number, department, doctor_type, is_emergency)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        patient_id,
        token_number,
        department,
        doctor_type,
        1 if is_emergency else 0,
    ))
    conn.commit()
    conn.close()
    print(f"[DB] Token saved: {token_number} → {department}")
    return token_number


# ─────────────────────────────────────────────────────────────────
# SAVE COMPLETE REGISTRATION (All-in-one helper)
# ─────────────────────────────────────────────────────────────────

def save_full_registration(session):
    """
    Master function – saves everything in one call.

    Parameter:
        session : dict with keys:
            name, age, gender, aadhaar_number,
            registration_type, symptoms,
            temperature, heart_rate, env,
            department, doctor_type, is_emergency

    Returns: dict – { patient_id, token_number }
    """
    # 1. Save patient
    patient_id = save_patient(
        name              = session.get("name", "Unknown"),
        age               = session.get("age", 0),
        gender            = session.get("gender", "Unknown"),
        aadhaar_number    = session.get("aadhaar_number", ""),
        registration_type = session.get("registration_type", "Temporary"),
    )

    # 2. Save health record
    save_health_record(
        patient_id  = patient_id,
        temperature = session.get("temperature"),
        heart_rate  = session.get("heart_rate"),
        env         = session.get("env", {}),
    )

    # 3. Save symptoms
    save_symptoms(
        patient_id = patient_id,
        symptoms   = session.get("symptoms", []),
    )

    # 4. Save token
    token_number = save_token(
        patient_id   = patient_id,
        department   = session.get("department", "General Medicine"),
        doctor_type  = session.get("doctor_type", "General Practitioner"),
        is_emergency = session.get("is_emergency", False),
    )

    return {
        "patient_id"   : patient_id,
        "token_number" : token_number,
    }


# ─────────────────────────────────────────────────────────────────
# FETCH PATIENT SUMMARY (for display on token screen)
# ─────────────────────────────────────────────────────────────────

def get_patient_summary(patient_id):
    """
    Fetches complete patient details for the token summary screen.
    Returns: dict with all patient info
    """
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()

    # Patient info
    c.execute('''
        SELECT name, age, gender, registration_type, created_at
        FROM patients WHERE patient_id = ?
    ''', (patient_id,))
    patient = c.fetchone()

    # Health record
    c.execute('''
        SELECT temperature, heart_rate, amb_temp, humidity, pressure
        FROM health_records WHERE patient_id = ?
        ORDER BY record_id DESC LIMIT 1
    ''', (patient_id,))
    health = c.fetchone()

    # Token
    c.execute('''
        SELECT token_number, department, doctor_type, is_emergency, issued_at
        FROM tokens WHERE patient_id = ?
        ORDER BY token_id DESC LIMIT 1
    ''', (patient_id,))
    token = c.fetchone()

    conn.close()

    return {
        "name"             : patient[0] if patient else "Unknown",
        "age"              : patient[1] if patient else "--",
        "gender"           : patient[2] if patient else "--",
        "registration_type": patient[3] if patient else "--",
        "registered_at"    : patient[4] if patient else "--",
        "temperature"      : health[0]  if health  else "--",
        "heart_rate"       : health[1]  if health  else "--",
        "amb_temp"         : health[2]  if health  else "--",
        "humidity"         : health[3]  if health  else "--",
        "pressure"         : health[4]  if health  else "--",
        "token_number"     : token[0]   if token   else "--",
        "department"       : token[1]   if token   else "--",
        "doctor_type"      : token[2]   if token   else "--",
        "is_emergency"     : bool(token[3]) if token else False,
        "issued_at"        : token[4]   if token   else "--",
    }
