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
    FONT_HEADING, FONT_NORMAL, FONT_SMALL, FONT_TINY,
    COLOR_GLASS
)
from utils.logger import get_logger
from sensors import beep
from utils.report_generator import generate_print_report
import qrcode
from PIL import Image, ImageTk
import io

log = get_logger("token_screen")


class TokenScreen(BaseScreen):
    """Final registration summary and token screen using CustomTkinter."""

    def show(self):
        self.clear()

        session = self.app.controller.get_session()
        is_emergency = session.get("is_emergency", False)

        # 1. Complete DB Save FIRST (Logical Step)
        try:
            result = self.app.controller.complete_registration()
            token  = result["token_number"]
            log.info(f"TokenScreen: Displaying token {token}")
        except Exception as e:
            log.error(f"Critical Fail in registration finish: {e}")
            token = "ERR-SAVE"

        # 2. Title / Header
        title = self.translate("emergency_title", "🚨 EMERGENCY ALERT") if is_emergency else self.translate("token_title")
        self.make_header(title)

        # 3. Main Content Wrapper
        container = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        container.pack(fill="both", expand=True)

        try:
            # Show Footer
            self.make_footer(self.translate("token_sub") + f" {session.get('name', 'Patient')}!")

            # Columns
            left = ctk.CTkFrame(container, fg_color="transparent")
            left.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            right = ctk.CTkFrame(container, fg_color="transparent")
            right.pack(side="right", fill="both", expand=True, padx=(10, 0))

            # LEFT: Patient Identity & QR
            name_display = (session.get("name") or "PATIENT").upper()
            id_card = ctk.CTkFrame(left, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
            id_card.pack(fill="both", expand=True)
            
            ctk.CTkLabel(id_card, text=name_display, font=("Segoe UI", 18, "bold"), text_color=COLOR_PRIMARY).pack(pady=(15, 0))
            ctk.CTkLabel(id_card, text=f"TOKEN: {token}", font=("Segoe UI", 32, "bold"), text_color=COLOR_ACCENT).pack(pady=(0, 10))
            
            # Robust QR Generation
            try:
                qr_data = f"TOKEN:{token}|NAME:{name_display}|DEPT:{session.get('department')}"
                qr = qrcode.QRCode(box_size=4, border=1)
                qr.add_data(qr_data)
                qr.make(fit=True)
                # Two-stage rendering for stability - get the underlying PIL image
                qr_pil = qr.make_image(fill_color="black", back_color="white").get_image()
                qr_img = ctk.CTkImage(light_image=qr_pil, size=(140, 140))
                ctk.CTkLabel(id_card, image=qr_img, text="").pack(pady=5)
            except Exception as qr_err:
                log.error(f"QR Display Error: {qr_err}")
                ctk.CTkLabel(id_card, text="[QR CODE UNAVAILABLE]", font=FONT_TINY).pack(pady=10)

            ctk.CTkLabel(id_card, text="DIGITAL RECEIPT QR", font=FONT_TINY, text_color=COLOR_TEXT_LIGHT).pack(pady=(0, 15))

            # RIGHT: Clinical Report Card
            rep_card = ctk.CTkFrame(right, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color=COLOR_BORDER)
            rep_card.pack(fill="both", expand=True, pady=(0, 10))

            ctk.CTkLabel(rep_card, text="CLINICAL SUMMARY", font=FONT_SMALL, text_color=COLOR_PRIMARY).pack(pady=5)
            
            # Vitals Dashboard (Unified Row format)
            v_frame = ctk.CTkFrame(rep_card, fg_color="#F8FAFC", corner_radius=8)
            v_frame.pack(fill="x", padx=10, pady=5)
            t = session.get('temperature', '--')
            h = session.get('heart_rate', '--')
            s = session.get('spo2', '--')
            v_str = f"🌡 {t}°C   |   💓 {h} BPM   |   🩸 {s}%"
            ctk.CTkLabel(v_frame, text=v_str, font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT).pack(pady=5)

            # Routing Info
            m_frame = ctk.CTkFrame(rep_card, fg_color="transparent")
            m_frame.pack(fill="x", padx=15, pady=2)
            
            clinical_details = [
                ("Department:", session.get("department") or "General"),
                ("Doctor:",     session.get("doctor_type") or "Resident"),
                ("Diagnosis:",  (session.get("severity") or "Normal") + " Observation"),
            ]
            
            for i, (l, v) in enumerate(clinical_details):
                ctk.CTkLabel(m_frame, text=l, font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_LIGHT).grid(row=i, column=0, sticky="e", pady=2)
                ctk.CTkLabel(m_frame, text=v, font=("Segoe UI", 10), text_color=COLOR_TEXT, wraplength=130, anchor="w", justify="left").grid(row=i, column=1, sticky="w", pady=2, padx=10)

            # Action Buttons Area
            btn_area = ctk.CTkFrame(right, fg_color="transparent")
            btn_area.pack(fill="x")
            
            self.make_button(btn_area, text="🖨 Print Receipt", command=lambda: self._print_token(session), color=COLOR_ACCENT, height=42).pack(fill="x", pady=2)
            self.make_button(btn_area, text="⭐ Rate Experience", command=self._show_feedback_dialog, color=COLOR_PRIMARY, height=42).pack(fill="x", pady=2)
            self.make_button(btn_area, text="🔄 New Registration", command=lambda: self.app.show_screen("welcome"), color=COLOR_PRIMARY, height=42).pack(fill="x", pady=2)

        except Exception as e:
            # Emergency Error Display
            err_box = ctk.CTkFrame(container, fg_color="#FFF0F0", border_width=1, border_color=COLOR_DANGER)
            err_box.pack(expand=True, padx=40, pady=40)
            ctk.CTkLabel(err_box, text="❌ ERROR SAVING DATA", font=FONT_HEADING, text_color=COLOR_DANGER).pack(pady=10)
            ctk.CTkLabel(err_box, text=str(e), font=FONT_TINY, text_color=COLOR_TEXT).pack(pady=10)
            self.make_button(err_box, text="🔄 Try Again / Restart", command=lambda: self.app.show_screen("welcome"), color=COLOR_PRIMARY).pack(pady=10)

        beep(3)

    def _print_token(self, session):
        generate_print_report(session)
        messagebox.showinfo("Print", "Token sent to printer!\n(Check console in Mock Mode)")

    def _show_feedback_dialog(self):
        """Shows a popup to collect patient feedback."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Patient Feedback")
        dialog.geometry("400x300")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="How was your experience?", font=FONT_HEADING).pack(pady=10)
        
        rating_var = ctk.IntVar(value=5)
        stars_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        stars_frame.pack(pady=5)
        
        for i in range(1, 6):
            ctk.CTkRadioButton(stars_frame, text=str(i), variable=rating_var, value=i, width=40).pack(side="left", padx=5)
            
        comment_box = ctk.CTkEntry(dialog, placeholder_text="Any comments? (Optional)", width=300)
        comment_box.pack(pady=20)
        
        def submit():
            rating = rating_var.get()
            comments = comment_box.get()
            
            # Use threading to not block UI
            import threading
            import requests
            import json
            
            def post_feedback():
                try:
                    requests.post("http://localhost:8080/api/feedback", 
                                 json={"rating": rating, "comments": comments}, 
                                 timeout=3)
                except: pass
            
            threading.Thread(target=post_feedback, daemon=True).start()
            messagebox.showinfo("Thank You", "Thank you for your feedback!")
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Submit Feedback", command=submit, fg_color=COLOR_ACCENT).pack(pady=10)
