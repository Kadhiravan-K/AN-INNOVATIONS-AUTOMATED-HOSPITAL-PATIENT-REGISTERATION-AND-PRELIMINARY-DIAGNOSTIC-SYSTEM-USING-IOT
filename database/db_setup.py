# ─────────────────────────────────────────────────────────────────
# database/db_setup.py — Database initialization
# ─────────────────────────────────────────────────────────────────

import sqlite3
from config import DB_PATH
from utils.logger import get_logger

log = get_logger("database")


def init_database():
    """
    Creates all required tables in the SQLite database.
    Safe to call multiple times — uses CREATE IF NOT EXISTS.
    """
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()

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

    c.execute('''
        CREATE TABLE IF NOT EXISTS symptoms (
            symptom_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id   INTEGER,
            symptom_code TEXT,
            recorded_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

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
    log.info("Database initialised successfully.")
