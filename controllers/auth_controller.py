# ─────────────────────────────────────────────────────────────────
# controllers/auth_controller.py — Authentication flow wrapper
# ─────────────────────────────────────────────────────────────────

from auth import send_otp, verify_otp, get_patient_demographics
from utils.logger import get_logger

log = get_logger("controller.auth")


class AuthController:
    """Wraps auth module with GUI-friendly interface."""

    def initiate_otp(self, aadhaar_number):
        """
        Validate and send OTP for the given Aadhaar.
        Returns: (bool, str) — (success, message)
        """
        success, msg = send_otp(aadhaar_number)
        if success:
            log.info("OTP sent for Aadhaar ending %s", aadhaar_number[-4:])
        return success, msg

    def verify(self, otp_code):
        """
        Verify the entered OTP.
        Returns: (bool, str) — (success, message)
        """
        success, msg = verify_otp(otp_code)
        if success:
            log.info("OTP verification successful.")
        return success, msg

    def get_demographics(self, aadhaar_number):
        """
        Fetch patient demographics after OTP verification.
        Returns: dict — { name, age, gender, address }
        """
        demographics = get_patient_demographics(aadhaar_number)
        log.info("Demographics fetched: %s", demographics.get("name", "Unknown"))
        return demographics
