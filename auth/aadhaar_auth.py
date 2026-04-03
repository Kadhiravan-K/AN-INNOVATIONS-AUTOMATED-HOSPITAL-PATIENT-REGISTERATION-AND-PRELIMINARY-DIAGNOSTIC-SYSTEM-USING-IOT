# ─────────────────────────────────────────────────────────────────
# AADHAAR AUTHENTICATION SERVICE (Mock & Real API)
# ─────────────────────────────────────────────────────────────────

import time
import random
import hashlib
from config import MOCK_MODE
from utils.logger import get_logger

log = get_logger("auth.aadhaar")

# ── Private State (OTP storage) ──────────────────────────────────
_current_otp  = None
_otp_attempts = 0
MAX_ATTEMPTS  = 3


# ─────────────────────────────────────────────────────────────────
# VALIDATE AADHAAR
# ─────────────────────────────────────────────────────────────────

def validate_aadhaar(number):
    """Basic format validation for Aadhaar number."""
    if not number or len(number) != 12 or not number.isdigit():
        return False, "Aadhaar must be a 12-digit number."
    return True, ""


# ─────────────────────────────────────────────────────────────────
# REQUEST OTP
# ─────────────────────────────────────────────────────────────────

def send_otp(aadhaar_number):
    """Alias for request_otp to maintain compatibility."""
    return request_otp(aadhaar_number)

def request_otp(aadhaar_number):
    """
    Sends an OTP request to UIDAI (or simulates it).
    Returns: (bool, str) — (success, message)
    """
    global _current_otp, _otp_attempts
    _otp_attempts = 0 # Reset attempts

    if not aadhaar_number or len(aadhaar_number) != 12:
        return False, "Invalid Aadhaar number format."

    if MOCK_MODE:
        time.sleep(1) # Simulate network lag
        _current_otp = str(random.randint(100000, 999999))
        log.info(f"MOCK OTP for {aadhaar_number}: {_current_otp}")
        return True, "OTP sent successfully to registered mobile!"

    else:
        try:
            # Placeholder for real UIDAI API integration
            import requests
            
            API_URL = "https://api.uidai.gov.in/otp/request/1.0"
            API_KEY = "YOUR_API_KEY_HERE"
            
            payload = {
                "uid"   : aadhaar_number,
                "txnId" : f"TXN{random.randint(100000, 999999)}",
                "ver"   : "2.0",
            }
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type" : "application/json",
            }
            
            # response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
            # if response.status_code == 200: return True, "OTP Sent!"
            
            return False, "UIDAI API Credentials Missing. Use MOCK_MODE."

        except Exception as e:
            log.error("OTP send error: %s", e)
            return False, f"Network error: {str(e)}"


# ─────────────────────────────────────────────────────────────────
# RESET AUTH STATE
# ─────────────────────────────────────────────────────────────────

def reset_auth():
    """Resets the OTP attempts and current OTP."""
    global _current_otp, _otp_attempts
    _current_otp = None
    _otp_attempts = 0


# ─────────────────────────────────────────────────────────────────
# VERIFY OTP
# ─────────────────────────────────────────────────────────────────

def verify_otp(entered_otp):
    """
    Verifies the OTP entered by the patient.
    Returns: (bool, str) — (success, message)
    """
    global _current_otp, _otp_attempts

    otp = entered_otp.strip()
    if not otp.isdigit() or len(otp) != 6:
        return False, "OTP must be exactly 6 digits."

    if MOCK_MODE:
        log.info(f"Mock OTP verification: entered={otp}, current={_current_otp}")
        _current_otp  = None
        _otp_attempts = 0
        return True, "Aadhaar authentication successful!"

    _otp_attempts += 1
    remaining = MAX_ATTEMPTS - _otp_attempts

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
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type" : "application/json",
        }

        # response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        return False, "UIDAI API Credentials Missing. Use MOCK_MODE."

    except Exception as e:
        log.error("OTP verify error: %s", e)
        return False, f"Network error: {str(e)}"


# ─────────────────────────────────────────────────────────────────
# GET PATIENT DEMOGRAPHICS
# ─────────────────────────────────────────────────────────────────

def get_patient_demographics(aadhaar_number):
    """
    Fetches patient demographic details after successful OTP.
    Returns: dict — { name, age, gender, address }
    """
    if MOCK_MODE:
        time.sleep(1)
        return {
            "name"   : "Demo Patient",
            "age"    : random.randint(18, 75),
            "gender" : random.choice(["Male", "Female"]),
            "address": "Coimbatore, Tamil Nadu",
        }

    else:
        try:
            import requests
            API_URL = "https://api.uidai.gov.in/demographics/1.0"
            API_KEY = "YOUR_API_KEY_HERE"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type" : "application/json",
            }
            payload = {"uid": aadhaar_number}

            # response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
            return None

        except Exception as e:
            log.error("Demographic fetch error: %s", e)
            return None
