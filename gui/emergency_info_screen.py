# ─────────────────────────────────────────────────────────────────
# gui/emergency_info_screen.py — Emergency Patient Details Form
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import messagebox
from gui.base_screen import BaseScreen
from config import COLOR_DANGER, COLOR_SURFACE, COLOR_CARD, COLOR_TEXT, COLOR_TEXT_LIGHT, FONT_HEADING, FONT_NORMAL
from sensors import beep

class EmergencyInfoScreen(BaseScreen):
    def show(self):
        self.clear()
        self.make_header("🚨 Emergency Registration")
        self.make_footer("Emergency Registration - Quick Processing")

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        # ── Buttons (pack FIRST so they never get clipped) ───────
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=(4, 8))

        self.make_button(
            btn_frame, text="←  Back",
            command=lambda: self.app.show_screen("welcome"),
            color=COLOR_TEXT_LIGHT, width=140,
        ).grid(row=0, column=0, padx=8)

        self.make_button(
            btn_frame, text="Next  →",
            command=self._save_and_next,
            color=COLOR_DANGER, width=140,
        ).grid(row=0, column=1, padx=8)

        # ── Title ────────────────────────────────────────────────
        ctk.CTkLabel(content, text="🚨 Enter Emergency Admission Details",
                     font=FONT_HEADING, text_color=COLOR_DANGER).pack(pady=(8, 4))

        # ── Form Card ────────────────────────────────────────────
        _, form_card = self.make_card(content, padx=15, pady=4)
        form_card.pack(pady=4, padx=20)

        session = self.app.controller.get_session()

        # Admission Number
        self._make_field(form_card, "Admission No *", 0)
        self.adm_var = ctk.StringVar()
        self.make_entry(form_card, textvariable=self.adm_var, width=250, font=FONT_NORMAL, justify="left").grid(row=0, column=1, pady=4, padx=10)

        # Patient Name
        self._make_field(form_card, "Patient Name (Optional)", 1)
        self.name_var = ctk.StringVar()
        self.make_entry(form_card, textvariable=self.name_var, width=250, font=FONT_NORMAL, justify="left").grid(row=1, column=1, pady=4, padx=10)

        # Status
        self._make_field(form_card, "Identity Status", 2)
        self.status_var = ctk.StringVar(value="Known")
        status_menu = ctk.CTkOptionMenu(master=form_card, values=["Known", "Unknown"], variable=self.status_var, font=FONT_NORMAL, width=250)
        status_menu.grid(row=2, column=1, pady=4, padx=10, sticky="w")

        # Attender Name
        self._make_field(form_card, "Attender Name", 3)
        self.att_name_var = ctk.StringVar()
        self.make_entry(form_card, textvariable=self.att_name_var, width=250, font=FONT_NORMAL, justify="left").grid(row=3, column=1, pady=4, padx=10)

        # Attender Phone
        self._make_field(form_card, "Attender Phone", 4)
        self.att_phone_var = ctk.StringVar()
        self.make_entry(form_card, textvariable=self.att_phone_var, width=250, font=FONT_NORMAL, justify="left").grid(row=4, column=1, pady=4, padx=10)

    def _make_field(self, parent, label, row):
        ctk.CTkLabel(parent, text=f"{label} :", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT, anchor="e", width=160).grid(row=row, column=0, pady=6, padx=(10, 10), sticky="e")

    def _save_and_next(self):
        adm_no = self.adm_var.get().strip()
        p_name = self.name_var.get().strip()
        a_name = self.att_name_var.get().strip()
        a_phone = self.att_phone_var.get().strip()

        if not adm_no:
            messagebox.showwarning("Required", "Admission Number is compulsory.")
            return

        if not p_name:
            if not a_name or not a_phone:
                messagebox.showwarning("Required", "Because Patient Name is missing, Attender Name AND Phone are compulsory.")
                return

        final_name = p_name if p_name else f"Unknown ({self.status_var.get()})"

        self.app.controller.save_patient_info(
            name=final_name,
            age="0", # Age is unknown usually for emergencies, default to 0
            gender="Unknown",
            visit_type="Emergency"
        )
        self.app.controller.session["is_emergency"] = True
        self.app.controller.session["admission_no"] = adm_no
        self.app.controller.session["attender_name"] = a_name
        self.app.controller.session["attender_phone"] = a_phone
        
        beep(1)
        self.app.show_screen("symptoms")
