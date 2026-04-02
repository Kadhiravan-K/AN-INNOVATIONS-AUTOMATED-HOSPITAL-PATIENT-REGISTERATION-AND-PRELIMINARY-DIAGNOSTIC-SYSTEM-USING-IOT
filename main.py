# ─────────────────────────────────────────────────────────────────
# main.py — Entry Point for Hospital Patient Registration Kiosk (CTk)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN, COLOR_SURFACE,
    SCREEN_TIMEOUT_MS
)
from database.db_setup import init_database
from controllers.registration_controller import RegistrationController
from controllers.sensor_controller import SensorController
from controllers.auth_controller import AuthController
from sensors import cleanup
from services.admin_server import start_admin_dashboard
from utils.logger import get_logger

# Screen modules
from gui.welcome_screen import WelcomeScreen
from gui.aadhaar_screen import AadhaarScreen
from gui.patient_info_screen import PatientInfoScreen
from gui.emergency_info_screen import EmergencyInfoScreen
from gui.symptom_screen import SymptomScreen
from gui.health_screen import HealthScreen
from gui.token_screen import TokenScreen
from gui.maintenance_screen import MaintenanceScreen

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
            "maintenance" : MaintenanceScreen(self),
        }

        self.current_screen = None
        self._timeout_id = None

        # ── Global Activity Monitor ──────────────────────────────
        self.root.bind("<Button-1>", lambda e: self.reset_timeout())
        self.root.bind("<Key>", lambda e: self.reset_timeout())

        # ── Initialise database ──────────────────────────────────
        init_database()

        # ── Start Admin Dashboard (Web) ──────────────────────────
        start_admin_dashboard(port=8080)

        # ── Start Status Poller (Remote Enable/Disable) ──────────
        self.is_offline = False
        self._poll_remote_status()

        # ── Show first screen ────────────────────────────────────
        self.show_screen("welcome")

    def show_screen(self, screen_name):
        """Navigate to a screen by name."""
        # If offline, force maintenance screen
        if self.is_offline and screen_name != "maintenance":
            screen_name = "maintenance"

        self.current_screen = screen_name
        
        if screen_name == "welcome":
            self.controller.start_session()
            self._cancel_timeout() # No timeout on welcome screen
        elif screen_name == "maintenance":
            self._cancel_timeout()
        else:
            self.reset_timeout()

        screen = self.screens.get(screen_name)
        if screen:
            screen.show()
            log.info("Screen: %s", screen_name)
        else:
            log.error("Unknown screen: %s", screen_name)

    def _poll_remote_status(self):
        """Background task to check if admin has disabled the kiosk."""
        import urllib.request
        import json
        try:
            with urllib.request.urlopen("http://localhost:8080/api/status", timeout=1) as response:
                data = json.loads(response.read().decode())
                online = data.get("online", True)
                
                if not online and not self.is_offline:
                    log.warning("Kiosk remotely DISABLED by admin.")
                    self.is_offline = True
                    self.show_screen("maintenance")
                elif online and self.is_offline:
                    log.info("Kiosk remotely ENABLED by admin.")
                    self.is_offline = False
                    self.show_screen("welcome")
        except Exception as e:
            # If server isn't up yet or fails, assume online but log it
            pass
        
        # Poll every 5 seconds
        self.root.after(5000, self._poll_remote_status)

    def reset_timeout(self):
        """Resets the inactivity timer."""
        self._cancel_timeout()
        if self.current_screen != "welcome":
            self._timeout_id = self.root.after(SCREEN_TIMEOUT_MS, self._on_timeout)

    def _cancel_timeout(self):
        if self._timeout_id:
            self.root.after_cancel(self._timeout_id)
            self._timeout_id = None

    def _on_timeout(self):
        """Called when session times out."""
        log.warning("Session timeout reached. Resetting to Welcome.")
        self.show_screen("welcome")

    def center_window(self, win, width, height):
        """Utility to center a Toplevel or window on the screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")


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