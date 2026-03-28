# ─────────────────────────────────────────────────────────────────
# gui/patient_info_screen.py — Patient Details Form (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import messagebox
import datetime
from gui.base_screen import BaseScreen
from config import (
    COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_BORDER,
    FONT_HEADING, FONT_NORMAL, FONT_SMALL,
)
from sensors import beep

class PatientInfoScreen(BaseScreen):
    """Patient information form screen."""

    def show(self):
        self.clear()
        self.make_header("Patient Information")
        self.make_footer()

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        ctk.CTkLabel(content, text="👤", font=("Segoe UI", 32), text_color=COLOR_TEXT).pack(pady=(10, 2))
        ctk.CTkLabel(content, text="Please confirm / enter your details", font=FONT_HEADING, text_color=COLOR_TEXT).pack(pady=(0, 10))

        # ── Form Card ────────────────────────────────────────────
        _, form_card = self.make_card(content, padx=15, pady=5)
        form_card.pack(pady=5)
        
        session = self.app.controller.get_session()

        # Name
        self._make_field(form_card, "Full Name", 0)
        self.name_var = ctk.StringVar(value=session.get("name", ""))

        def validate_name(*args):
            val = self.name_var.get()
            filtered = "".join([c for c in val if c.isalpha() or c.isspace()])
            if val != filtered:
                self.name_var.set(filtered)

        self.name_var.trace_add("write", validate_name)

        self.make_entry(
            form_card, textvariable=self.name_var,
            width=250, font=FONT_NORMAL, justify="left",
        ).grid(row=0, column=1, pady=8, padx=10)

        # Date of Birth
        self._make_field(form_card, "Date of Birth (DD/MM/YYYY)", 1)
        self.dob_var = ctk.StringVar(value="")

        def format_dob(*args):
            val = self.dob_var.get()
            digits = "".join(filter(str.isdigit, val))
            if len(digits) > 8:
                digits = digits[:8]
            
            out = ""
            if len(digits) > 0:
                out += digits[:2]
            if len(digits) >= 3:
                out += "/" + digits[2:4]
            if len(digits) >= 5:
                out += "/" + digits[4:]
            
            if val != out:
                self.dob_var.set(out)

        self.dob_var.trace_add("write", format_dob)

        self.make_entry(
            form_card, textvariable=self.dob_var,
            width=250, font=FONT_NORMAL, justify="left",
        ).grid(row=1, column=1, pady=6, padx=10)

        # Gender
        self._make_field(form_card, "Gender", 2)
        self.gender_var = ctk.StringVar(value=session.get("gender", "Male"))
        gender_menu = ctk.CTkOptionMenu(
            master=form_card,
            values=["Male", "Female", "Other"],
            variable=self.gender_var,
            font=FONT_NORMAL,
            width=250,
            fg_color=COLOR_CARD,
            button_color=COLOR_ACCENT,
            button_hover_color=self._darken(COLOR_ACCENT),
            text_color=COLOR_TEXT,
        )
        # Fix border explicitly if CTk allows
        gender_menu.grid(row=2, column=1, pady=6, padx=10, sticky="w")

        # Visit Type
        self._make_field(form_card, "Visit Type", 3)
        self.visit_var = ctk.StringVar(value="Outpatient (OPD)")
        visit_menu = ctk.CTkOptionMenu(
            master=form_card,
            values=["Outpatient (OPD)", "Re-checkup", "Emergency"],
            variable=self.visit_var,
            font=FONT_NORMAL,
            width=250,
            fg_color=COLOR_CARD,
            button_color=COLOR_ACCENT,
            button_hover_color=self._darken(COLOR_ACCENT),
            text_color=COLOR_TEXT,
        )
        visit_menu.grid(row=3, column=1, pady=6, padx=10, sticky="w")

        # ── Buttons ──────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=5)

        self.make_button(
            btn_frame, text="←  Back",
            command=lambda: self.app.show_screen("welcome"),
            color=COLOR_TEXT_LIGHT, width=140,
        ).grid(row=0, column=0, padx=8)

        self.make_button(
            btn_frame, text="Next  →",
            command=self._save_and_next,
            color=COLOR_ACCENT, width=140,
        ).grid(row=0, column=1, padx=8)

    def _make_field(self, parent, label, row):
        """Create a form field label."""
        ctk.CTkLabel(
            parent, text=f"{label} :",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="e", width=120,
        ).grid(row=row, column=0, pady=8, padx=(10, 10), sticky="e")

    def _save_and_next(self):
        name = self.name_var.get().strip()
        dob_str = self.dob_var.get().strip()

        if not name:
            messagebox.showwarning("Required", "Please enter patient name.")
            return
            
        try:
            dob = datetime.datetime.strptime(dob_str, "%d/%m/%Y")
            today = datetime.datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0 or age > 150:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid", "Please enter a valid Date of Birth (DD/MM/YYYY).")
            return

        self.app.controller.save_patient_info(
            name, str(age), self.gender_var.get(), self.visit_var.get()
        )
        beep(1)
        self.app.show_screen("symptoms")
