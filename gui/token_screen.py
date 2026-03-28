# ─────────────────────────────────────────────────────────────────
# gui/token_screen.py — Final Token & Summary Screen (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import messagebox
import datetime
from gui.base_screen import BaseScreen
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_SUCCESS, COLOR_DANGER,
    COLOR_BORDER,
    FONT_HEADING, FONT_NORMAL, FONT_SMALL,
)
from sensors import beep
from utils.report_generator import generate_print_report


class TokenScreen(BaseScreen):
    """Final registration summary and token screen using CustomTkinter."""

    def show(self):
        self.clear()

        session = self.app.controller.get_session()
        is_emergency = session.get("is_emergency", False)

        result = self.app.controller.complete_registration()
        token  = result["token_number"]

        if is_emergency:
            self.make_header("🚨  EMERGENCY – See Staff Immediately")
        else:
            self.make_header("✅  Registration Complete")

        self.make_footer(
            f"Thank you, {session.get('name', 'Patient')}! "
            f"Please proceed to {session.get('department', 'the department')}."
        )

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        # ── Token Card ───────────────────────────────────────────
        card_bg = "#FFF0F0" if is_emergency else COLOR_CARD
        _, token_card = self.make_card(content, padx=15, pady=5, bg=card_bg)
        # Re-pack it with standard sizing 
        token_card.pack(pady=5, fill="x", padx=40)

        token_color = COLOR_DANGER if is_emergency else COLOR_ACCENT
        ctk.CTkLabel(
            token_card,
            text=f"TOKEN: {token}",
            font=("Segoe UI", 22, "bold"),
            text_color=token_color,
        ).pack(pady=(2, 5))

        # Separator
        sep = ctk.CTkFrame(token_card, height=1, fg_color=COLOR_BORDER)
        sep.pack(fill="x", pady=2)

        # Details grid inside another frame to align properties
        details_frame = ctk.CTkFrame(token_card, fg_color="transparent")
        details_frame.pack(pady=5)

        details = [
            ("Patient Name",  session.get("name", "--")),
            ("Age / Gender",
             f"{session.get('age', '--')} yrs  |  "
             f"{session.get('gender', '--')}"),
            ("Department",    session.get("department", "--")),
            ("Doctor Type",   session.get("doctor_type", "--")),
            ("Temperature",   f"{session.get('temperature', '--')} °C"),
            ("Heart Rate",    f"{session.get('heart_rate', '--')} BPM"),
            ("Visit Type",    session.get("visit_type", "--")),
            ("Date & Time",   datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")),
        ]

        for i, (label, value) in enumerate(details):
            row = i % 4
            col_offset = (i // 4) * 2

            ctk.CTkLabel(
                details_frame,
                text=f"{label} :",
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_TEXT,
                anchor="e", width=110,
            ).grid(row=row, column=col_offset, sticky="e", pady=1, padx=(10, 5))

            ctk.CTkLabel(
                details_frame,
                text=value,
                font=("Segoe UI", 12),
                text_color="#333333",
                anchor="w", width=120,
            ).grid(row=row, column=col_offset + 1, sticky="w", pady=1)

        if is_emergency:
            ctk.CTkLabel(
                content,
                text="⚠  CRITICAL VALUES DETECTED – Inform staff immediately!",
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_DANGER,
            ).pack(pady=2)

        beep(3)

        # ── Bottom Buttons ───────────────────────────────────────
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=5)

        self.make_button(
            btn_frame, text="🔄  New Registration",
            command=lambda: self.app.show_screen("welcome"),
            color=COLOR_PRIMARY, width=160,
        ).grid(row=0, column=0, padx=10)

        self.make_button(
            btn_frame, text="🖨  Print Token",
            command=lambda: self._print_token(session),
            color=COLOR_ACCENT, width=160,
        ).grid(row=0, column=1, padx=10)

    def _print_token(self, session):
        generate_print_report(session)
        messagebox.showinfo("Print", "Token sent to printer!\n(Check console in Mock Mode)")
