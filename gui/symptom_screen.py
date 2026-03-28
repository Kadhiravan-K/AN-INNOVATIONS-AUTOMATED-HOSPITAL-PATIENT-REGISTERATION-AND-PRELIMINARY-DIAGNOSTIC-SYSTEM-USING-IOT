# ─────────────────────────────────────────────────────────────────
# gui/symptom_screen.py — Symptom Selection Screen (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from gui.base_screen import BaseScreen
from config import (
    COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_PRIMARY,
    FONT_HEADING, FONT_NORMAL, FONT_SMALL,
    SYMPTOM_LABELS, SYMPTOM_CATEGORIES,
)
from sensors import beep

class SymptomScreen(BaseScreen):
    """Modern symptom selection with categorized card layout."""

    def show(self):
        self.clear()
        self.make_header("Select Symptoms")
        self.make_footer("Select all that apply — you can select multiple")

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        ctk.CTkLabel(
            content, text="Please select all applicable symptoms",
            font=FONT_HEADING, text_color=COLOR_TEXT,
        ).pack(pady=(8, 5))

        # ── Symptom area ──────────────────────────────
        self.symptom_vars = {}

        symptom_frame = ctk.CTkScrollableFrame(content, fg_color="transparent", orientation="horizontal", height=200)
        symptom_frame.pack(pady=5, fill="both", expand=True, padx=5)

        # In CTk, grid works fine. Let's arrange them in a wrapped or scrollable frame.
        col = 0
        for category, codes in SYMPTOM_CATEGORIES.items():
            # Category card
            _, cat_card = self.make_card(symptom_frame, padx=10, pady=8)
            cat_card.grid(row=0, column=col, padx=10, pady=5, sticky="n")

            # Category title
            ctk.CTkLabel(
                cat_card, text=category,
                font=("Segoe UI", 16, "bold"),
                text_color=COLOR_PRIMARY,
            ).pack(anchor="w", pady=(0, 5), padx=5)

            # Symptom checkboxes
            for code in codes:
                label = SYMPTOM_LABELS.get(code, code)
                var = ctk.BooleanVar()
                self.symptom_vars[code] = var

                cb = ctk.CTkCheckBox(
                    master=cat_card,
                    text=label,
                    variable=var,
                    font=("Segoe UI", 16),
                    text_color=COLOR_TEXT,
                    checkbox_width=24,
                    checkbox_height=24,
                    border_width=2,
                    border_color=COLOR_PRIMARY,
                    hover_color=COLOR_ACCENT,
                    fg_color=COLOR_ACCENT,
                    corner_radius=4
                )
                cb.pack(anchor="w", pady=4, padx=5)

            col += 1

        # ── Buttons ──────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=8)

        self.make_button(
            btn_frame, text="←  Back",
            command=lambda: self.app.show_screen("patient_info"),
            color=COLOR_TEXT_LIGHT, width=140,
        ).grid(row=0, column=0, padx=8)

        self.make_button(
            btn_frame, text="Next – Health Check  →",
            command=self._save_and_next,
            color=COLOR_ACCENT, width=200,
        ).grid(row=0, column=1, padx=8)

    def _save_and_next(self):
        selected = [
            code for code, var in self.symptom_vars.items()
            if var.get()
        ]
        if not selected:
            from tkinter import messagebox
            messagebox.showwarning("Required", "Please select at least 1 symptom before continuing.")
            return

        self.app.controller.save_symptoms(selected)
        beep(1)
        self.app.show_screen("health")
