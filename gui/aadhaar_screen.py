# ─────────────────────────────────────────────────────────────────
# gui/aadhaar_screen.py — Aadhaar Entry + OTP (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from tkinter import messagebox
from gui.base_screen import BaseScreen
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_SUCCESS, COLOR_DANGER,
    COLOR_BORDER,
    FONT_HEADING, FONT_NORMAL, FONT_SMALL,
)
from sensors import beep

class AadhaarScreen(BaseScreen):
    """Aadhaar entry and OTP verification screen using CustomTkinter."""

    def show(self):
        self._show_aadhaar_entry()

    # ─────────────────────────────────────────────────────────────
    # VIEW 1: Aadhaar Number Entry
    # ─────────────────────────────────────────────────────────────
    def _show_aadhaar_entry(self):
        self.clear()
        self.make_header("Identity Verification")
        self.make_footer("Enter Aadhaar → Receive OTP → Verify")

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
            btn_frame, text="Send OTP  →",
            command=self._handle_send_otp,
            color=COLOR_ACCENT, width=140,
        ).grid(row=0, column=1, padx=8)

        # ── Status label (pack from bottom too) ──────────────────
        self.status_label = self.make_status_label(content)
        self.status_label.pack(side="bottom", pady=4)

        # ── Title ────────────────────────────────────────────────
        ctk.CTkLabel(content, text="🆔 Enter your 12-digit Aadhaar Number",
                     font=FONT_HEADING, text_color=COLOR_TEXT).pack(pady=(12, 8))

        # ── Entry Card ───────────────────────────────────────────
        _, entry_card = self.make_card(content, padx=15, pady=8)
        entry_card.pack(pady=5, padx=30)

        self.aadhaar_var = ctk.StringVar()

        def limit_aadhaar(*args):
            val = self.aadhaar_var.get()
            filtered = "".join(filter(str.isdigit, val))
            if len(filtered) > 12:
                filtered = filtered[:12]
            if val != filtered:
                self.aadhaar_var.set(filtered)

        self.aadhaar_var.trace_add("write", limit_aadhaar)

        # Entry + eye button in a horizontal row
        entry_row = ctk.CTkFrame(entry_card, fg_color="transparent")
        entry_row.pack(pady=(10, 8))

        self.aadhaar_entry = self.make_entry(
            entry_row,
            textvariable=self.aadhaar_var,
            width=250, show="●",
            font=("Consolas", 20),
        )
        self.aadhaar_entry.pack(side="left", padx=(0, 5))
        self.aadhaar_entry.focus()

        self._show_aadhaar = False
        def toggle_show():
            self._show_aadhaar = not self._show_aadhaar
            self.aadhaar_entry.configure(show="" if self._show_aadhaar else "●")
            self.eye_btn.configure(text="👁" if self._show_aadhaar else "👁‍🗨")

        self.eye_btn = ctk.CTkButton(
            entry_row, text="👁‍🗨", width=40, height=40,
            fg_color="transparent", font=("Segoe UI", 22),
            text_color=COLOR_TEXT, hover_color=COLOR_BORDER,
            command=toggle_show, corner_radius=8,
        )
        self.eye_btn.pack(side="left")

    def _handle_send_otp(self):
        aadhaar = self.aadhaar_var.get().strip()
        success, msg = self.app.auth_ctrl.initiate_otp(aadhaar)

        if success:
            self.app.controller.save_aadhaar(aadhaar)
            beep(1)
            messagebox.showinfo("OTP Sent", msg)
            self._show_otp_verify()
        else:
            self.status_label.configure(text=msg, text_color=COLOR_DANGER)
            beep(2)

    # ─────────────────────────────────────────────────────────────
    # VIEW 2: OTP Verification
    # ─────────────────────────────────────────────────────────────
    def _show_otp_verify(self):
        self.clear()
        self.make_header("Enter OTP")
        self.make_footer("Check console for OTP (Mock Mode)")

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        session = self.app.controller.get_session()
        aadhaar = session.get("aadhaar_number", "")
        masked  = f"XXXX-XXXX-{aadhaar[-4:]}" if len(aadhaar) >= 4 else "----"

        ctk.CTkLabel(content, text="📱", font=("Segoe UI", 36), text_color=COLOR_TEXT).pack(pady=(15, 5))
        ctk.CTkLabel(content, text=f"OTP sent for Aadhaar: {masked}", font=FONT_HEADING, text_color=COLOR_TEXT).pack()
        ctk.CTkLabel(content, text="Enter the 6-digit OTP received on your mobile", font=FONT_NORMAL, text_color=COLOR_TEXT_LIGHT).pack(pady=(5, 10))

        _, otp_card = self.make_card(content, padx=15, pady=10)
        otp_card.pack(pady=5)
        
        self.otp_var = ctk.StringVar()

        def limit_otp(*args):
            val = self.otp_var.get()
            filtered = "".join(filter(str.isdigit, val))
            if len(filtered) > 6:
                filtered = filtered[:6]
            if val != filtered:
                self.otp_var.set(filtered)

        self.otp_var.trace_add("write", limit_otp)

        otp_entry = self.make_entry(
            otp_card,
            textvariable=self.otp_var,
            width=150,
            font=("Consolas", 24),
        )
        otp_entry.pack(pady=15)
        otp_entry.focus()

        self.otp_status = self.make_status_label(content)
        self.otp_status.pack(pady=5)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.make_button(
            btn_frame, text="Resend OTP",
            command=self._show_aadhaar_entry,
            color=COLOR_TEXT_LIGHT, width=140,
        ).grid(row=0, column=0, padx=8)

        self.make_button(
            btn_frame, text="✔  Verify OTP",
            command=self._handle_verify_otp,
            color=COLOR_SUCCESS, width=140,
        ).grid(row=0, column=1, padx=8)

    def _handle_verify_otp(self):
        otp = self.otp_var.get().strip()
        success, msg = self.app.auth_ctrl.verify(otp)

        if success:
            beep(2)
            session = self.app.controller.get_session()
            demographics = self.app.auth_ctrl.get_demographics(session.get("aadhaar_number", ""))
            self.app.controller.update_demographics(demographics)
            messagebox.showinfo("Verified ✔", msg)
            self.app.show_screen("patient_info")
        else:
            beep(3)
            self.otp_status.configure(text=msg, text_color=COLOR_DANGER)
