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
            spo2         REAL,
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
            severity     TEXT,
            is_emergency INTEGER DEFAULT 0,
            status       TEXT    DEFAULT "waiting",
            issued_at    TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating      INTEGER,
            comments    TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── Migrations (Safe column additions) ────────────────
    def add_col_if_missing(table, col, def_val=""):
        try:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col}")
            log.info(f"Migration: Added column {col} to {table}")
        except sqlite3.OperationalError:
            pass # Already exists

    add_col_if_missing("patients", "allergies", "''")
    add_col_if_missing("patients", "medical_history", "''")
    add_col_if_missing("patients", "last_visit_id", "0")
    add_col_if_missing("tokens", "severity", "'Normal'")
    add_col_if_missing("health_records", "spo2", "0.0")

    conn.commit()
    conn.close()
    log.info("Database initialised and migrated successfully.")
