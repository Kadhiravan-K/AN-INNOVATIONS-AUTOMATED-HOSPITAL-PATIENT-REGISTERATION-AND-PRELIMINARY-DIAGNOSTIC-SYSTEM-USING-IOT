# ─────────────────────────────────────────────────────────────────
# database/db_operations.py — All CRUD operations
# ─────────────────────────────────────────────────────────────────

import sqlite3
import hashlib
from config import DB_PATH
from utils.logger import get_logger
from utils.token_generator import generate_token_number

log = get_logger("database")


# ─────────────────────────────────────────────────────────────────
# SAVE PATIENT RECORD
# ─────────────────────────────────────────────────────────────────

def save_patient(name, age, gender, aadhaar_number, registration_type):
    """
    Saves a new patient record. Aadhaar is stored as SHA-256 hash.
    Returns: int — newly created patient_id
    """
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

    log.info("Patient saved. ID: %d", patient_id)
    return patient_id


# ─────────────────────────────────────────────────────────────────
# SAVE HEALTH RECORD
# ─────────────────────────────────────────────────────────────────

def save_health_record(patient_id, temperature, heart_rate, env):
    """Saves sensor readings linked to a patient."""
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
    log.info("Health record saved for patient ID: %d", patient_id)


# ─────────────────────────────────────────────────────────────────
# SAVE SYMPTOMS
# ─────────────────────────────────────────────────────────────────

def save_symptoms(patient_id, symptoms):
    """Saves all selected symptom codes for a patient."""
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    for symptom in symptoms:
        c.execute('''
            INSERT INTO symptoms (patient_id, symptom_code)
            VALUES (?, ?)
        ''', (patient_id, symptom))
    conn.commit()
    conn.close()
    log.info("%d symptom(s) saved for patient ID: %d", len(symptoms), patient_id)


# ─────────────────────────────────────────────────────────────────
# SAVE TOKEN
# ─────────────────────────────────────────────────────────────────

def save_token(patient_id, department, doctor_type, is_emergency):
    """Generates and saves a registration token. Returns: str — token number."""
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
    log.info("Token saved: %s → %s", token_number, department)
    return token_number


# ─────────────────────────────────────────────────────────────────
# SAVE COMPLETE REGISTRATION (All-in-one)
# ─────────────────────────────────────────────────────────────────

def save_full_registration(session):
    """
    Master function — saves everything in one call.
    Returns: dict — { patient_id, token_number }
    """
    patient_id = save_patient(
        name              = session.get("name", "Unknown"),
        age               = session.get("age", 0),
        gender            = session.get("gender", "Unknown"),
        aadhaar_number    = session.get("aadhaar_number", ""),
        registration_type = session.get("registration_type", "Temporary"),
    )

    save_health_record(
        patient_id  = patient_id,
        temperature = session.get("temperature"),
        heart_rate  = session.get("heart_rate"),
        env         = session.get("env", {}),
    )

    save_symptoms(
        patient_id = patient_id,
        symptoms   = session.get("symptoms", []),
    )

    token_number = save_token(
        patient_id   = patient_id,
        department   = session.get("department", "General Medicine"),
        doctor_type  = session.get("doctor_type", "General Practitioner"),
        is_emergency = session.get("is_emergency", False),
    )

    return {
        "patient_id"  : patient_id,
        "token_number": token_number,
    }


# ─────────────────────────────────────────────────────────────────
# FETCH PATIENT SUMMARY
# ─────────────────────────────────────────────────────────────────

def get_patient_summary(patient_id):
    """Fetches complete patient details for the token summary screen."""
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()

    c.execute('''
        SELECT name, age, gender, registration_type, created_at
        FROM patients WHERE patient_id = ?
    ''', (patient_id,))
    patient = c.fetchone()

    c.execute('''
        SELECT temperature, heart_rate, amb_temp, humidity, pressure
        FROM health_records WHERE patient_id = ?
        ORDER BY record_id DESC LIMIT 1
    ''', (patient_id,))
    health = c.fetchone()

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
