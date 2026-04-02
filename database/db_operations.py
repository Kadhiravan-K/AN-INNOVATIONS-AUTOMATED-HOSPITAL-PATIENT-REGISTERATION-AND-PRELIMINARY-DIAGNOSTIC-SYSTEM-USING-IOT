# ─────────────────────────────────────────────────────────────────
# database/db_operations.py — All CRUD operations
# ─────────────────────────────────────────────────────────────────

import sqlite3
import hashlib
from config import DB_PATH, SECRET_SALT
from utils.logger import get_logger
from utils.token_generator import generate_token_number

log = get_logger("database")


# ─────────────────────────────────────────────────────────────────
# SAVE PATIENT RECORD
# ─────────────────────────────────────────────────────────────────

def save_patient(name, age, gender, aadhaar_number, registration_type, allergies="", medical_history=""):
    """
    Saves a new patient record. Aadhaar is stored as salted SHA-256 hash.
    Returns: int — newly created patient_id
    """
    aadhaar_hash = None
    if aadhaar_number:
        # Use salt to prevent rainbow table attacks
        salted = f"{aadhaar_number}{SECRET_SALT}"
        aadhaar_hash = hashlib.sha256(salted.encode()).hexdigest()

    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO patients (name, age, gender, aadhaar_hash, registration_type, allergies, medical_history)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, aadhaar_hash, registration_type, allergies, medical_history))

    patient_id = c.lastrowid
    conn.commit()
    conn.close()

    log.info("Patient saved. ID: %d", patient_id)
    return patient_id


# ─────────────────────────────────────────────────────────────────
# SAVE HEALTH RECORD
# ─────────────────────────────────────────────────────────────────

def save_health_record(patient_id, temperature, heart_rate, spo2, env):
    """Saves sensor readings linked to a patient."""
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO health_records
            (patient_id, temperature, heart_rate, spo2, amb_temp, humidity, pressure)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        patient_id,
        temperature,
        heart_rate,
        spo2,
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

def save_token(patient_id, department, doctor_type, severity, is_emergency):
    """Generates and saves a registration token. Returns: str — token number."""
    token_number = generate_token_number()

    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute('''
        INSERT INTO tokens
            (patient_id, token_number, department, doctor_type, severity, is_emergency)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        patient_id,
        token_number,
        department,
        doctor_type,
        severity,
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
    try:
        patient_id = save_patient(
            name              = session.get("name", "Unknown"),
            age               = session.get("age", 0),
            gender            = session.get("gender", "Unknown"),
            aadhaar_number    = session.get("aadhaar_number", ""),
            registration_type = session.get("registration_type", "Temporary"),
            allergies         = session.get("allergies", ""),
            medical_history   = session.get("medical_history", "")
        )

        try:
            save_health_record(
                patient_id  = patient_id,
                temperature = session.get("temperature"),
                heart_rate  = session.get("heart_rate"),
                spo2        = session.get("spo2"),
                env         = session.get("env", {}),
            )
        except Exception as e:
            log.error(f"Health Save Error: {e}")

        try:
            save_symptoms(
                patient_id = patient_id,
                symptoms   = session.get("symptoms", []),
            )
        except Exception as e:
            log.error(f"Symptoms Save Error: {e}")

        token_number = save_token(
            patient_id   = patient_id,
            department   = session.get("department", "General Medicine"),
            doctor_type  = session.get("doctor_type", "General Practitioner"),
            severity     = session.get("severity", "Normal"),
            is_emergency = session.get("is_emergency", False),
        )

        return {
            "patient_id"  : patient_id,
            "token_number": token_number,
        }
    except Exception as e:
        log.error(f"CRITICAL DB SAVE ERROR: {e}")
        # Return fallback data to keep UI alive
        return {"patient_id": 0, "token_number": "ERR-SAVE"}


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
        SELECT temperature, heart_rate, spo2, amb_temp, humidity, pressure
        FROM health_records WHERE patient_id = ?
        ORDER BY record_id DESC LIMIT 1
    ''', (patient_id,))
    health = c.fetchone()

    c.execute('''
        SELECT token_number, department, doctor_type, severity, is_emergency, issued_at
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
        "spo2"             : health[2]  if health  else "--",
        "amb_temp"         : health[3]  if health  else "--",
        "humidity"         : health[4]  if health  else "--",
        "pressure"         : health[5]  if health  else "--",
        "token_number"     : token[0]   if token   else "--",
        "department"       : token[1]   if token   else "--",
        "doctor_type"      : token[2]   if token   else "--",
        "severity"         : token[3]   if token   else "Normal",
        "is_emergency"     : bool(token[4]) if token else False,
        "issued_at"        : token[5]   if token   else "--",
    }
def get_previous_visit_by_aadhaar(aadhaar_number):
    """Finds last visit info using salted Aadhaar hash."""
    if not aadhaar_number: return None
    
    salted = f"{aadhaar_number}{SECRET_SALT}"
    aadhaar_hash = hashlib.sha256(salted.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c    = conn.cursor()
        
        # Get patient details and latest token
        c.execute('''
            SELECT p.patient_id, p.name, p.allergies, p.medical_history, t.issued_at, t.token_number
            FROM patients p
            LEFT JOIN tokens t ON p.patient_id = t.patient_id
            WHERE p.aadhaar_hash = ?
            ORDER BY t.issued_at DESC LIMIT 1
        ''', (aadhaar_hash,))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                "patient_id": row[0], "name": row[1],
                "allergies": row[2], "medical_history": row[3],
                "last_visit_at": row[4], "last_token": row[5]
            }
        return None
    except Exception as e:
        log.error(f"Error fetching historical data: {e}")
        return None
