# ─────────────────────────────────────────────────────────────────
# auth.py
# Project  : Automated Hospital Patient Registration System
# College  : Hindusthan College of Engineering and Technology
# Dept     : Electrical and Electronics Engineering
# Guide    : Dr. R. Rajeshkanna
# ─────────────────────────────────────────────────────────────────

import random
import time
from .config import MOCK_MODE

# ─────────────────────────────────────────────────────────────────
# HOW THIS WORKS
# ─────────────────────────────────────────────────────────────────
# MOCK MODE  (MOCK_MODE = True)
#   → Simulates OTP send & verify on your laptop
#   → No internet needed
#   → Any 6-digit number works as OTP
#
# REAL MODE  (MOCK_MODE = False)
#   → Calls actual UIDAI Aadhaar API
#   → Requires government registration & API key
#   → For production hospital use only
# ─────────────────────────────────────────────────────────────────


# Internal storage for the generated OTP (session only)
_current_otp  = None
_otp_attempts = 0
MAX_ATTEMPTS  = 3


# ─────────────────────────────────────────────────────────────────
# VALIDATE AADHAAR FORMAT
# ─────────────────────────────────────────────────────────────────

def validate_aadhaar(aadhaar_number):
    """
    Validates the format of an Aadhaar number.
    Rules:
      - Must be exactly 12 digits
      - Must contain only numbers
      - Must not start with 0 or 1

    Returns: (bool, str) – (is_valid, message)
    """
    aadhaar = aadhaar_number.strip()

    if not aadhaar.isdigit():
        return False, "Aadhaar number must contain digits only."

    if len(aadhaar) != 12:
        return False, "Aadhaar number must be exactly 12 digits."

    if aadhaar[0] in ("0", "1"):
        return False, "Invalid Aadhaar number format."

    return True, "Valid"


# ─────────────────────────────────────────────────────────────────
# SEND OTP
# ─────────────────────────────────────────────────────────────────

def send_otp(aadhaar_number):
    """
    Sends an OTP to the mobile number linked with the Aadhaar.

    MOCK MODE  → Generates a random 6-digit OTP internally.
                 Prints it to console (for testing).
    REAL MODE  → Calls UIDAI API to trigger real OTP.

    Returns: (bool, str) – (success, message)
    """
    global _current_otp, _otp_attempts

    # ── Validate Aadhaar first ────────────────────────────────────
    is_valid, msg = validate_aadhaar(aadhaar_number)
    if not is_valid:
        return False, msg

    # ── Reset attempt counter ─────────────────────────────────────
    _otp_attempts = 0

    if MOCK_MODE:
        # ── MOCK: Generate random 6-digit OTP ────────────────────
        _current_otp = str(random.randint(100000, 999999))
        time.sleep(1)  # simulate API delay

        # Print OTP to console so you can test
        print(f"\n{'='*40}")
        print(f"  [MOCK OTP]  Your OTP is: {_current_otp}")
        print(f"{'='*40}\n")

        return True, (
            f"OTP sent successfully!\n"
            f"(Mock Mode: Check console for OTP)\n"
            f"Aadhaar: XXXX-XXXX-{aadhaar_number[-4:]}"
        )

    else:
        # ── REAL: Call UIDAI Aadhaar API ──────────────────────────
        try:
            import requests

            # NOTE: Replace with your actual UIDAI API credentials
            API_URL    = "https://api.uidai.gov.in/otp/1.0"
            API_KEY    = "YOUR_API_KEY_HERE"
            APP_ID     = "YOUR_APP_ID_HERE"

            payload = {
                "uid"    : aadhaar_number,
                "txnId"  : f"TXN{random.randint(100000, 999999)}",
                "ac"     : APP_ID,
                "sa"     : APP_ID,
                "ver"    : "2.0",
                "ts"     : time.strftime("%Y-%m-%dT%H:%M:%S"),
                "type"   : "otp",
            }
            headers = {
                "Authorization" : f"Bearer {API_KEY}",
                "Content-Type"  : "application/json",
            }

            response = requests.post(
                API_URL,
                json    = payload,
                headers = headers,
                timeout = 10,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return True, (
                        f"OTP sent to your registered mobile.\n"
                        f"Aadhaar: XXXX-XXXX-{aadhaar_number[-4:]}"
                    )
                else:
                    return False, f"Failed to send OTP: {data.get('message','Unknown error')}"
            else:
                return False, f"API Error: {response.status_code}"

        except Exception as e:
            return False, f"Network error: {str(e)}"


# ─────────────────────────────────────────────────────────────────
# VERIFY OTP
# ─────────────────────────────────────────────────────────────────

def verify_otp(entered_otp):
    """
    Verifies the OTP entered by the patient.

    MOCK MODE  → Compares with internally generated OTP.
    REAL MODE  → Validates with UIDAI API.

    Returns: (bool, str) – (success, message)
    """
    global _current_otp, _otp_attempts

    # ── Check OTP format ─────────────────────────────────────────
    otp = entered_otp.strip()
    if not otp.isdigit() or len(otp) != 6:
        return False, "OTP must be exactly 6 digits."

    # ── Track attempts ────────────────────────────────────────────
    _otp_attempts += 1
    remaining = MAX_ATTEMPTS - _otp_attempts

    if MOCK_MODE:
        # ── MOCK: Compare with stored OTP ─────────────────────────
        if _current_otp is None:
            return False, "No OTP generated. Please request a new OTP."

        if otp == _current_otp:
            _current_otp  = None   # clear OTP after success
            _otp_attempts = 0
            return True, "Identity verified successfully!"
        else:
            if remaining <= 0:
                _current_otp  = None
                _otp_attempts = 0
                return False, "Too many failed attempts. Please try again."
            return False, f"Incorrect OTP. {remaining} attempt(s) remaining."

    else:
        # ── REAL: Validate with UIDAI API ─────────────────────────
        try:
            import requests

            API_URL = "https://api.uidai.gov.in/otp/verify/1.0"
            API_KEY = "YOUR_API_KEY_HERE"
            APP_ID  = "YOUR_APP_ID_HERE"

            payload = {
                "otp"   : otp,
                "txnId" : f"TXN{random.randint(100000, 999999)}",
                "ac"    : APP_ID,
                "ver"   : "2.0",
                "ts"    : time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            headers = {
                "Authorization" : f"Bearer {API_KEY}",
                "Content-Type"  : "application/json",
            }

            response = requests.post(
                API_URL,
                json    = payload,
                headers = headers,
                timeout = 10,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    _otp_attempts = 0
                    return True, "Identity verified successfully!"
                else:
                    if remaining <= 0:
                        return False, "Too many failed attempts. Please try again."
                    return False, f"Incorrect OTP. {remaining} attempt(s) remaining."
            else:
                return False, f"API Error: {response.status_code}"

        except Exception as e:
            return False, f"Network error: {str(e)}"


# ─────────────────────────────────────────────────────────────────
# GET PATIENT DEMOGRAPHICS (after successful OTP)
# ─────────────────────────────────────────────────────────────────

def get_patient_demographics(aadhaar_number):
    """
    Fetches patient demographic details after successful OTP.

    MOCK MODE  → Returns fake demo data for testing.
    REAL MODE  → Fetches masked data from UIDAI API.

    Returns: dict – { name, age, gender, address }
    """
    if MOCK_MODE:
        # Return simulated patient data
        time.sleep(1)
        return {
            "name"    : "Demo Patient",
            "age"     : random.randint(18, 75),
            "gender"  : random.choice(["Male", "Female"]),
            "address" : "Coimbatore, Tamil Nadu",
        }

    else:
        # ── REAL: Fetch from UIDAI API ────────────────────────────
        try:
            import requests

            API_URL = "https://api.uidai.gov.in/demographics/1.0"
            API_KEY = "YOUR_API_KEY_HERE"

            headers = {
                "Authorization" : f"Bearer {API_KEY}",
                "Content-Type"  : "application/json",
            }
            payload = { "uid": aadhaar_number }

            response = requests.post(
                API_URL,
                json    = payload,
                headers = headers,
                timeout = 10,
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "name"    : data.get("name", "Unknown"),
                    "age"     : data.get("age", "--"),
                    "gender"  : data.get("gender", "--"),
                    "address" : data.get("address", "--"),
                }
            else:
                return {
                    "name"    : "Unknown",
                    "age"     : "--",
                    "gender"  : "--",
                    "address" : "--",
                }

        except Exception as e:
            print(f"[ERROR] Demographics fetch: {e}")
            return {
                "name"    : "Unknown",
                "age"     : "--",
                "gender"  : "--",
                "address" : "--",
            }


# ─────────────────────────────────────────────────────────────────
# RESET SESSION
# ─────────────────────────────────────────────────────────────────

def reset_auth():
    """
    Clears OTP and attempt counter.
    Call this when starting a new patient registration.
    """
    global _current_otp, _otp_attempts
    _current_otp  = None
    _otp_attempts = 0
    print("[AUTH] Session reset.")
