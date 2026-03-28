# ─────────────────────────────────────────────────────────────────
# gui/welcome_screen.py — Welcome / Registration Type Selection (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from gui.base_screen import BaseScreen
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_DANGER, FONT_HEADING, FONT_NORMAL, FONT_SMALL
)
from sensors import beep


class WelcomeScreen(BaseScreen):
    """Welcome screen with two registration options."""

    def show(self):
        self.clear()
        self.make_header("Welcome to Patient Registration")
        self.make_footer()

        # ── Main content area ────────────────────────────────────
        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        # Welcome icon
        ctk.CTkLabel(
            content,
            text="🏥",
            font=("Segoe UI", 48),
            text_color=COLOR_TEXT
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            content,
            text="Please select your registration type",
            font=FONT_HEADING,
            text_color=COLOR_TEXT,
        ).pack(pady=(0, 20))

        # ── Cards container ──────────────────────────────────────
        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(pady=5)

        # ── Permanent Registration Card ──────────────────────────
        _, perm_card = self.make_card(cards_frame, padx=10, pady=10)
        perm_card.grid(row=0, column=0, padx=8)

        ctk.CTkLabel(
            perm_card, text="🔒", font=("Segoe UI", 32),
            text_color=COLOR_PRIMARY
        ).pack(pady=(5, 0))

        ctk.CTkLabel(
            perm_card, text="Permanent",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_PRIMARY,
        ).pack(pady=(5, 2))

        self.make_button(
            perm_card, text="Select",
            command=self._go_permanent,
            color=COLOR_PRIMARY, width=120, height=35,
            font=FONT_NORMAL,
        ).pack(pady=(5, 10))

        # ── Temporary Registration Card ──────────────────────────
        _, temp_card = self.make_card(cards_frame, padx=10, pady=10)
        temp_card.grid(row=0, column=1, padx=8)

        ctk.CTkLabel(
            temp_card, text="⏱", font=("Segoe UI", 32),
            text_color=COLOR_ACCENT
        ).pack(pady=(5, 0))

        ctk.CTkLabel(
            temp_card, text="Temporary",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_ACCENT,
        ).pack(pady=(5, 2))

        self.make_button(
            temp_card, text="Select",
            command=self._go_temporary,
            color=COLOR_ACCENT, width=120, height=35,
            font=FONT_NORMAL,
        ).pack(pady=(5, 10))

        # ── Emergency Registration Card ──────────────────────────
        _, emg_card = self.make_card(cards_frame, padx=10, pady=10)
        emg_card.grid(row=0, column=2, padx=8)

        ctk.CTkLabel(
            emg_card, text="🚨", font=("Segoe UI", 32),
            text_color=COLOR_DANGER
        ).pack(pady=(5, 0))

        ctk.CTkLabel(
            emg_card, text="Emergency",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_DANGER,
        ).pack(pady=(5, 2))

        self.make_button(
            emg_card, text="Select",
            command=self._go_emergency,
            color=COLOR_DANGER, width=120, height=35,
            font=FONT_NORMAL,
        ).pack(pady=(5, 10))


    # ── Actions ──────────────────────────────────────────────────

    def _go_permanent(self):
        beep(1)
        self.app.controller.set_registration_type("Permanent")
        self.app.show_screen("aadhaar")

    def _go_temporary(self):
        beep(1)
        self.app.controller.set_registration_type("Temporary")
        self.app.show_screen("patient_info")

    def _go_emergency(self):
        beep(1)
        self.app.controller.set_registration_type("Emergency")
        self.app.show_screen("emergency")
