# ─────────────────────────────────────────────────────────────────
# gui/health_screen.py — Health Parameter Measurement (CTk Version)
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
import threading
from gui.base_screen import BaseScreen
from config import (
    COLOR_ACCENT, COLOR_SURFACE, COLOR_CARD,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_SUCCESS, COLOR_WARNING,
    COLOR_DANGER, COLOR_PRIMARY,
    FONT_HEADING, FONT_NORMAL, FONT_SMALL,
)
from sensors import beep
from services.health_analysis import analyze_vitals_full
from services.i18n import i18n

class HealthScreen(BaseScreen):
    """Animated health parameter measurement screen using CustomTkinter."""

    def show(self):
        self.clear()
        self.make_header(self.translate("health_title"))
        self.make_footer(self.translate("btn_health_sub", "Please remain still during measurement"))

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        ctk.CTkLabel(
            content, text=self.translate("btn_health_desc", "Please follow the instructions below"),
            font=FONT_HEADING, text_color=COLOR_TEXT,
        ).pack(pady=(8, 5))

        # ── Measurement Cards ────────────────────────────────────
        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(pady=5)

        # Temperature card
        _, temp_card = self.make_card(cards_frame, padx=10, pady=5)
        temp_card.grid(row=0, column=0, padx=10)

        ctk.CTkLabel(temp_card, text="🌡", font=("Segoe UI", 28)).pack(pady=(10,0))
        ctk.CTkLabel(temp_card, text=self.translate("temp_label"), font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack()
        self.temp_var = ctk.StringVar(value="--")
        self.temp_label = ctk.CTkLabel(
            temp_card, textvariable=self.temp_var,
            font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_LIGHT,
        )
        self.temp_label.pack(pady=3)
        self.temp_status = ctk.CTkLabel(temp_card, text="...", font=FONT_SMALL, text_color=COLOR_TEXT_LIGHT)
        self.temp_status.pack(pady=(0,10))

        # Heart Rate card
        _, hr_card = self.make_card(cards_frame, padx=10, pady=5)
        hr_card.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(hr_card, text="❤", font=("Segoe UI", 28)).pack(pady=(10,0))
        ctk.CTkLabel(hr_card, text=self.translate("hr_label"), font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack()
        self.hr_var = ctk.StringVar(value="--")
        self.hr_label = ctk.CTkLabel(
            hr_card, textvariable=self.hr_var,
            font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_LIGHT,
        )
        self.hr_label.pack(pady=3)
        self.hr_status = ctk.CTkLabel(hr_card, text="...", font=FONT_SMALL, text_color=COLOR_TEXT_LIGHT)
        self.hr_status.pack(pady=(0,10))

        # SpO2 card (NEW)
        _, spo2_card = self.make_card(cards_frame, padx=10, pady=5)
        spo2_card.grid(row=0, column=2, padx=10)

        ctk.CTkLabel(spo2_card, text="🫁", font=("Segoe UI", 28)).pack(pady=(10,0))
        ctk.CTkLabel(spo2_card, text=self.translate("spo2_label"), font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack()
        self.spo2_var = ctk.StringVar(value="--")
        self.spo2_label = ctk.CTkLabel(
            spo2_card, textvariable=self.spo2_var,
            font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_LIGHT,
        )
        self.spo2_label.pack(pady=3)
        self.spo2_status = ctk.CTkLabel(spo2_card, text="...", font=FONT_SMALL, text_color=COLOR_TEXT_LIGHT)
        self.spo2_status.pack(pady=(0,10))

        # Status text
        self.health_status = ctk.CTkLabel(
            content, text=self.translate("status_reading"),
            font=FONT_NORMAL, text_color=COLOR_ACCENT,
        )
        self.health_status.pack(pady=10)

        # ── Start measurements ───────────────────────────────────
        threading.Thread(target=self._run_measurements, daemon=True).start()

    def _run_measurements(self):
        sensor_ctrl = self.app.sensor_ctrl

        self.root.after(0, lambda: self.health_status.configure(text="🌡  Measuring body temperature..."))
        self.root.after(0, lambda: self.progress.update_progress(0.1))

        temp = sensor_ctrl.get_temperature()

        self.root.after(0, lambda: self.temp_var.set(f"{temp} °C" if temp else "Err"))
        self.root.after(0, lambda: self.progress.update_progress(0.25))

        analysis = analyze_vitals_full(temp, None, None)
        color_map = {"normal": COLOR_SUCCESS, "warning": COLOR_WARNING, "critical": COLOR_DANGER}
        temp_color = color_map.get(analysis["temp_status"], COLOR_TEXT)
        self.root.after(0, lambda: self.temp_label.configure(text_color=temp_color))
        self.root.after(0, lambda: self.temp_status.configure(text=analysis["temp_message"], text_color=temp_color))

        # ── Heart Rate ──
        self.root.after(0, lambda: self.health_status.configure(text="❤  Measuring heart rate..."))
        hr = sensor_ctrl.get_heart_rate()
        self.root.after(0, lambda: self.hr_var.set(f"{hr} BPM" if hr else "Err"))
        self.root.after(0, lambda: self.progress.update_progress(0.50))
        analysis = analyze_vitals_full(None, hr, None)
        hr_color = color_map.get(analysis["hr_status"], COLOR_TEXT)
        self.root.after(0, lambda: self.hr_label.configure(text_color=hr_color))
        self.root.after(0, lambda: self.hr_status.configure(text=analysis["hr_message"], text_color=hr_color))

        # ── SpO2 ──
        self.root.after(0, lambda: self.health_status.configure(text="🫁  Measuring oxygen level..."))
        spo2 = sensor_ctrl.get_spo2()
        self.root.after(0, lambda: self.spo2_var.set(f"{spo2} %" if spo2 else "Err"))
        self.root.after(0, lambda: self.progress.update_progress(0.75))
        analysis = analyze_vitals_full(None, None, spo2)
        spo2_color = color_map.get(analysis["spo2_status"], COLOR_TEXT)
        self.root.after(0, lambda: self.spo2_label.configure(text_color=spo2_color))
        self.root.after(0, lambda: self.spo2_status.configure(text=analysis["spo2_message"], text_color=spo2_color))

        self.root.after(0, lambda: self.health_status.configure(text="🌤  Reading environment..."))

        env = sensor_ctrl.get_environment()

        self.root.after(0, lambda: self.progress.update_progress(1.0))

        self.app.controller.save_health_data(temp, hr, env, spo2=spo2)
        self.app.controller.perform_triage()

        self.root.after(0, lambda: self.health_status.configure(text="✅  Measurements complete!", text_color=COLOR_SUCCESS))
        beep(2)

        self.root.after(1500, lambda: self.app.show_screen("token"))
