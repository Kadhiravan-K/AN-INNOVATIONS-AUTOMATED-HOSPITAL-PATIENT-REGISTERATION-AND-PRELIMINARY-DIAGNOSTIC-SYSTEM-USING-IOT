# ─────────────────────────────────────────────────────────────────
# gui/maintenance_screen.py — Maintenance / Offline Screen
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from gui.base_screen import BaseScreen
from config import (
    COLOR_SURFACE, COLOR_TEXT, COLOR_PRIMARY, COLOR_WARNING,
    FONT_TITLE, FONT_HEADING, FONT_NORMAL
)

class MaintenanceScreen(BaseScreen):
    """Screen displayed when the kiosk is remotely disabled by admin."""

    def show(self):
        self.clear()
        
        # We don't use standard header/footer here for a 'locked' feel
        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        # Center content
        center = ctk.CTkFrame(content, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            center, text="🛠", font=("Segoe UI", 72)
        ).pack(pady=10)

        ctk.CTkLabel(
            center, text="SYSTEM UNDER MAINTENANCE",
            font=FONT_TITLE, text_color=COLOR_PRIMARY
        ).pack(pady=5)

        ctk.CTkLabel(
            center, text="The registration kiosk is temporarily disabled by admin.",
            font=FONT_NORMAL, text_color=COLOR_TEXT
        ).pack(pady=5)

        ctk.CTkLabel(
            center, text="Please wait or contact hospital staff for assistance.",
            font=FONT_SMALL, text_color=COLOR_TEXT, opacity=0.7
        ).pack(pady=20)

        # Animated heartbeat to show the app is still 'alive'
        self.pulse_label = ctk.CTkLabel(
            center, text="● Kiosk Status: Checking Connectivity...",
            font=("Segoe UI", 10), text_color=COLOR_WARNING
        )
        self.pulse_label.pack(pady=10)
