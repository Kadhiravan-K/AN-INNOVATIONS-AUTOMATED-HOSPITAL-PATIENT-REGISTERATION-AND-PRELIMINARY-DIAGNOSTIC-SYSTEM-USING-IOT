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
from services.health_analysis import analyze_vitals

class HealthScreen(BaseScreen):
    """Animated health parameter measurement screen using CustomTkinter."""

    def show(self):
        self.clear()
        self.make_header("Health Parameter Measurement")
        self.make_footer("Please remain still during measurement")

        content = ctk.CTkFrame(self.root, fg_color=COLOR_SURFACE, corner_radius=0)
        content.pack(fill="both", expand=True)

        ctk.CTkLabel(
            content, text="Please follow the instructions below",
            font=FONT_HEADING, text_color=COLOR_TEXT,
        ).pack(pady=(8, 5))

        # ── Measurement Cards ────────────────────────────────────
        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(pady=5)

        # Temperature card
        _, temp_card = self.make_card(cards_frame, padx=10, pady=5)
        temp_card.grid(row=0, column=0, padx=10)

        ctk.CTkLabel(temp_card, text="🌡", font=("Segoe UI", 28)).pack()
        ctk.CTkLabel(temp_card, text="Body Temperature", font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack()
        self.temp_var = ctk.StringVar(value="Waiting...")
        self.temp_label = ctk.CTkLabel(
            temp_card, textvariable=self.temp_var,
            font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_LIGHT,
        )
        self.temp_label.pack(pady=3)
        self.temp_status = ctk.CTkLabel(temp_card, text="Hold forehead near IR sensor", font=FONT_SMALL, text_color=COLOR_TEXT_LIGHT)
        self.temp_status.pack()

        # Heart Rate card
        _, hr_card = self.make_card(cards_frame, padx=10, pady=5)
        hr_card.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(hr_card, text="❤", font=("Segoe UI", 28)).pack()
        ctk.CTkLabel(hr_card, text="Heart Rate", font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack()
        self.hr_var = ctk.StringVar(value="Waiting...")
        self.hr_label = ctk.CTkLabel(
            hr_card, textvariable=self.hr_var,
            font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_LIGHT,
        )
        self.hr_label.pack(pady=3)
        self.hr_status = ctk.CTkLabel(hr_card, text="Place finger on pulse sensor", font=FONT_SMALL, text_color=COLOR_TEXT_LIGHT)
        self.hr_status.pack()

        # Environment card
        _, env_card = self.make_card(content, padx=10, pady=5)
        env_card.pack(pady=5, fill="x", padx=40)

        env_inner = ctk.CTkFrame(env_card, fg_color="transparent")
        env_inner.pack(fill="x")

        ctk.CTkLabel(env_inner, text="🌤  Environment", font=("Segoe UI", 12, "bold"), text_color=COLOR_PRIMARY).pack(side="left", padx=10)
        self.env_var = ctk.StringVar(value="Reading...")
        ctk.CTkLabel(env_inner, textvariable=self.env_var, font=FONT_NORMAL, text_color=COLOR_TEXT).pack(side="left", padx=10)

        # ── Progress Bar ─────────────────────────────────────────
        self.progress = self.make_progress_bar(content, width=500, height=10)
        self.progress.pack(pady=(15, 3))

        # Status text
        self.health_status = ctk.CTkLabel(
            content, text="⏳  Starting measurements...",
            font=FONT_NORMAL, text_color=COLOR_ACCENT,
        )
        self.health_status.pack(pady=3)

        # ── Start measurements ───────────────────────────────────
        threading.Thread(target=self._run_measurements, daemon=True).start()

    def _run_measurements(self):
        sensor_ctrl = self.app.sensor_ctrl

        self.root.after(0, lambda: self.health_status.configure(text="🌡  Measuring body temperature..."))
        self.root.after(0, lambda: self.progress.update_progress(0.1))

        temp = sensor_ctrl.get_temperature()

        self.root.after(0, lambda: self.temp_var.set(f"{temp} °C" if temp else "Error"))
        self.root.after(0, lambda: self.progress.update_progress(0.33))

        analysis = analyze_vitals(temp, None)
        color_map = {"normal": COLOR_SUCCESS, "warning": COLOR_WARNING, "critical": COLOR_DANGER}
        temp_color = color_map.get(analysis["temp_status"], COLOR_TEXT)
        self.root.after(0, lambda: self.temp_label.configure(text_color=temp_color))
        self.root.after(0, lambda: self.temp_status.configure(text=analysis["temp_message"], text_color=temp_color))

        self.root.after(0, lambda: self.health_status.configure(text="❤  Measuring heart rate – keep finger still..."))

        hr = sensor_ctrl.get_heart_rate()

        self.root.after(0, lambda: self.hr_var.set(f"{hr} BPM" if hr else "Error"))
        self.root.after(0, lambda: self.progress.update_progress(0.66))

        analysis = analyze_vitals(None, hr)
        hr_color = color_map.get(analysis["hr_status"], COLOR_TEXT)
        self.root.after(0, lambda: self.hr_label.configure(text_color=hr_color))
        self.root.after(0, lambda: self.hr_status.configure(text=analysis["hr_message"], text_color=hr_color))

        self.root.after(0, lambda: self.health_status.configure(text="🌤  Reading environment..."))

        env = sensor_ctrl.get_environment()

        self.root.after(0, lambda: self.env_var.set(
            f"Temp: {env['amb_temp']}°C  |  "
            f"Humidity: {env['humidity']}%  |  "
            f"Pressure: {env['pressure']} hPa"
        ))
        self.root.after(0, lambda: self.progress.update_progress(1.0))

        self.app.controller.save_health_data(temp, hr, env)
        self.app.controller.perform_triage()

        self.root.after(0, lambda: self.health_status.configure(text="✅  Measurements complete!", text_color=COLOR_SUCCESS))
        beep(2)

        self.root.after(1500, lambda: self.app.show_screen("token"))
