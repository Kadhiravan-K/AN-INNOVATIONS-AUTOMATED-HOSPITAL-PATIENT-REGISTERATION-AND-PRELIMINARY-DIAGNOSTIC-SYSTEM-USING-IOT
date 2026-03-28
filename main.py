# ─────────────────────────────────────────────────────────────────
# main.py — Entry Point for Hospital Patient Registration Kiosk (CTk)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN, COLOR_SURFACE
from database.db_setup import init_database
from controllers.registration_controller import RegistrationController
from controllers.sensor_controller import SensorController
from controllers.auth_controller import AuthController
from sensors import cleanup
from utils.logger import get_logger

# Screen modules
from gui.welcome_screen import WelcomeScreen
from gui.aadhaar_screen import AadhaarScreen
from gui.patient_info_screen import PatientInfoScreen
from gui.emergency_info_screen import EmergencyInfoScreen
from gui.symptom_screen import SymptomScreen
from gui.health_screen import HealthScreen
from gui.token_screen import TokenScreen

log = get_logger("app")


# ═════════════════════════════════════════════════════════════════
# CTK SETUP
# ═════════════════════════════════════════════════════════════════
ctk.set_appearance_mode("Light")  # We designed it specifically for a clean light/modern theme
ctk.set_default_color_theme("blue")  # Basic theme

# ═════════════════════════════════════════════════════════════════
# MAIN APPLICATION — Screen Navigator
# ═════════════════════════════════════════════════════════════════

class HospitalKioskApp:
    """
    Main application class. Acts as a screen navigator.
    Uses CustomTkinter for a profoundly modern look.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Patient Registration Kiosk")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        if FULLSCREEN:
            self.root.attributes("-fullscreen", True)

        # ── Controllers ──────────────────────────────────────────
        self.controller  = RegistrationController()
        self.sensor_ctrl = SensorController()
        self.auth_ctrl   = AuthController()

        # ── Screen registry ──────────────────────────────────────
        self.screens = {
            "welcome"     : WelcomeScreen(self),
            "aadhaar"     : AadhaarScreen(self),
            "patient_info": PatientInfoScreen(self),
            "emergency"   : EmergencyInfoScreen(self),
            "symptoms"    : SymptomScreen(self),
            "health"      : HealthScreen(self),
            "token"       : TokenScreen(self),
        }

        # ── Initialise database ──────────────────────────────────
        init_database()

        # ── Show first screen ────────────────────────────────────
        self.show_screen("welcome")

    def show_screen(self, screen_name):
        """Navigate to a screen by name."""
        if screen_name == "welcome":
            self.controller.start_session()

        screen = self.screens.get(screen_name)
        if screen:
            screen.show()
            log.info("Screen: %s", screen_name)
        else:
            log.error("Unknown screen: %s", screen_name)


# ═════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        root = ctk.CTk()
        app  = HospitalKioskApp(root)
        root.mainloop()
    finally:
        cleanup()
        log.info("Application closed.")