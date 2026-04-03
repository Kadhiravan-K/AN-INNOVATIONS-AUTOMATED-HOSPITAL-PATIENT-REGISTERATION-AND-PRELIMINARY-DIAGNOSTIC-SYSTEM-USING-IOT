# ─────────────────────────────────────────────────────────────────
# main.py
# Project  : Automated Hospital Patient Registration System
# ─────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox
import threading
import datetime

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN,
    COLOR_DARK, COLOR_BLUE, COLOR_LIGHT,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN,
    FONT_TITLE, FONT_HEADING, FONT_NORMAL, FONT_SMALL,
    SYMPTOM_LABELS, HOSPITAL_NAME, HOSPITAL_CITY,
)
from sensors   import (
    read_temperature, read_heart_rate,
    read_environment, allocate_department, beep, cleanup,
)
from database  import init_database, save_full_registration
from auth      import (
    validate_aadhaar, send_otp,
    verify_otp, get_patient_demographics, reset_auth,
)


# ═════════════════════════════════════════════════════════════════
# MAIN APPLICATION CLASS
# ═════════════════════════════════════════════════════════════════

class HospitalKioskApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Patient Registration Kiosk")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLOR_WHITE)
        self.root.resizable(False, False)

        if FULLSCREEN:
            self.root.attributes("-fullscreen", True)

        # ── Session data (reset for each new patient) ─────────────
        self.session = {}

        # ── Initialise database ───────────────────────────────────
        init_database()

        # ── Show first screen ─────────────────────────────────────
        self.show_welcome()


    # ─────────────────────────────────────────────────────────────
    # HELPER – Clear all widgets from screen
    # ─────────────────────────────────────────────────────────────

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    # ─────────────────────────────────────────────────────────────
    # HELPER – Top header bar (shown on every screen)
    # ─────────────────────────────────────────────────────────────

    def make_header(self, title):
        # College name bar
        tk.Label(
            self.root,
            text    = HOSPITAL_NAME,
            font    = ("Arial", 9, "bold"),
            bg      = COLOR_DARK,
            fg      = COLOR_WHITE,
            pady    = 4,
        ).pack(fill=tk.X)

        # Screen title bar
        tk.Label(
            self.root,
            text    = title,
            font    = FONT_TITLE,
            bg      = COLOR_BLUE,
            fg      = COLOR_WHITE,
            pady    = 10,
        ).pack(fill=tk.X)


    # ─────────────────────────────────────────────────────────────
    # HELPER – Bottom status bar
    # ─────────────────────────────────────────────────────────────

    def make_footer(self, text=""):
        tk.Label(
            self.root,
            text    = text or HOSPITAL_CITY,
            font    = FONT_SMALL,
            bg      = COLOR_DARK,
            fg      = COLOR_WHITE,
            pady    = 3,
        ).pack(side=tk.BOTTOM, fill=tk.X)


    # ─────────────────────────────────────────────────────────────
    # HELPER – Standard button
    # ─────────────────────────────────────────────────────────────

    def make_button(self, parent, text, command,
                    color=None, width=18, height=2):
        return tk.Button(
            parent,
            text            = text,
            command         = command,
            font            = FONT_HEADING,
            bg              = color or COLOR_BLUE,
            fg              = COLOR_WHITE,
            activebackground= COLOR_DARK,
            activeforeground= COLOR_WHITE,
            width           = width,
            height          = height,
            relief          = tk.FLAT,
            cursor          = "hand2",
        )


    # ─────────────────────────────────────────────────────────────
    # HELPER – Reset session for new patient
    # ─────────────────────────────────────────────────────────────

    def reset_session(self):
        self.session = {}
        reset_auth()


    # ═════════════════════════════════════════════════════════════
    # SCREEN 1 – WELCOME SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_welcome(self):
        self.clear()
        self.reset_session()

        self.make_header("Welcome to Patient Registration")

        # Welcome message
        tk.Label(
            self.root,
            text    = "Please select your registration type",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=20)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=10)

        # Permanent Registration button
        perm_btn = self.make_button(
            btn_frame,
            text    = "🏥  Permanent\nRegistration",
            command = self.go_permanent,
            color   = COLOR_DARK,
            width   = 20,
            height  = 4,
        )
        perm_btn.grid(row=0, column=0, padx=20)

        # Temporary Registration button
        temp_btn = self.make_button(
            btn_frame,
            text    = "🕐  Temporary\nRegistration",
            command = self.go_temporary,
            color   = COLOR_BLUE,
            width   = 20,
            height  = 4,
        )
        temp_btn.grid(row=0, column=1, padx=20)

        # Description labels
        tk.Label(
            btn_frame,
            text    = "With Aadhaar Verification",
            font    = FONT_SMALL,
            bg      = COLOR_WHITE,
            fg      = "grey",
        ).grid(row=1, column=0, pady=5)

        tk.Label(
            btn_frame,
            text    = "Privacy-Friendly Option",
            font    = FONT_SMALL,
            bg      = COLOR_WHITE,
            fg      = "grey",
        ).grid(row=1, column=1, pady=5)

        self.make_footer()


    # ─────────────────────────────────────────────────────────────

    def go_permanent(self):
        beep(1)
        self.session["registration_type"] = "Permanent"
        self.show_aadhaar_screen()

    def go_temporary(self):
        beep(1)
        self.session["registration_type"] = "Temporary"
        self.show_patient_info_screen()


    # ═════════════════════════════════════════════════════════════
    # SCREEN 2A – AADHAAR SCREEN (Permanent only)
    # ═════════════════════════════════════════════════════════════

    def show_aadhaar_screen(self):
        self.clear()
        self.make_header("Identity Verification – Aadhaar")

        tk.Label(
            self.root,
            text    = "Enter your 12-digit Aadhaar Number",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=15)

        # Aadhaar entry field
        self.aadhaar_var = tk.StringVar()
        entry = tk.Entry(
            self.root,
            textvariable    = self.aadhaar_var,
            font            = ("Arial", 20),
            width           = 16,
            show            = "•",
            justify         = tk.CENTER,
            relief          = tk.GROOVE,
            bd              = 2,
        )
        entry.pack(pady=8)
        entry.focus()

        # Show/hide toggle
        self.show_aadhaar = False
        def toggle_show():
            self.show_aadhaar = not self.show_aadhaar
            entry.config(show="" if self.show_aadhaar else "•")

        tk.Checkbutton(
            self.root,
            text     = "Show Aadhaar Number",
            font     = FONT_SMALL,
            bg       = COLOR_WHITE,
            command  = toggle_show,
        ).pack()

        # Status label
        self.aadhaar_status = tk.Label(
            self.root,
            text    = "",
            font    = FONT_SMALL,
            bg      = COLOR_WHITE,
            fg      = COLOR_RED,
        )
        self.aadhaar_status.pack(pady=4)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=10)

        self.make_button(
            btn_frame,
            text    = "Send OTP",
            command = self.handle_send_otp,
            color   = COLOR_BLUE,
        ).grid(row=0, column=0, padx=10)

        self.make_button(
            btn_frame,
            text    = "← Back",
            command = self.show_welcome,
            color   = COLOR_DARK,
        ).grid(row=0, column=1, padx=10)

        self.make_footer("Enter Aadhaar → Receive OTP → Verify")


    # ─────────────────────────────────────────────────────────────

    def handle_send_otp(self):
        aadhaar = self.aadhaar_var.get().strip()
        success, msg = send_otp(aadhaar)

        if success:
            self.session["aadhaar_number"] = aadhaar
            beep(1)
            messagebox.showinfo("OTP Sent", msg)
            self.show_otp_screen()
        else:
            self.aadhaar_status.config(text=msg, fg=COLOR_RED)
            beep(2)


    # ═════════════════════════════════════════════════════════════
    # SCREEN 2B – OTP VERIFICATION SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_otp_screen(self):
        self.clear()
        self.make_header("Enter OTP")

        masked = "XXXX-XXXX-" + self.session.get("aadhaar_number","")[-4:]

        tk.Label(
            self.root,
            text    = f"OTP sent for Aadhaar: {masked}",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=15)

        tk.Label(
            self.root,
            text    = "Enter the 6-digit OTP received on your mobile",
            font    = FONT_NORMAL,
            bg      = COLOR_WHITE,
        ).pack()

        # OTP entry
        self.otp_var = tk.StringVar()
        otp_entry = tk.Entry(
            self.root,
            textvariable = self.otp_var,
            font         = ("Arial", 24),
            width        = 10,
            justify      = tk.CENTER,
            relief       = tk.GROOVE,
            bd           = 2,
        )
        otp_entry.pack(pady=12)
        otp_entry.focus()

        # Status label
        self.otp_status = tk.Label(
            self.root,
            text = "",
            font = FONT_SMALL,
            bg   = COLOR_WHITE,
            fg   = COLOR_RED,
        )
        self.otp_status.pack(pady=4)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=8)

        self.make_button(
            btn_frame,
            text    = "✔  Verify OTP",
            command = self.handle_verify_otp,
            color   = COLOR_GREEN,
        ).grid(row=0, column=0, padx=10)

        self.make_button(
            btn_frame,
            text    = "Resend OTP",
            command = self.show_aadhaar_screen,
            color   = COLOR_DARK,
        ).grid(row=0, column=1, padx=10)

        self.make_footer("Check console/terminal for OTP (Mock Mode)")


    # ─────────────────────────────────────────────────────────────

    def handle_verify_otp(self):
        otp = self.otp_var.get().strip()
        success, msg = verify_otp(otp)

        if success:
            beep(2)
            # Fetch demographics
            demographics = get_patient_demographics(
                self.session.get("aadhaar_number", "")
            )
            self.session.update(demographics)
            messagebox.showinfo("Verified ✔", msg)
            self.show_patient_info_screen()
        else:
            beep(3)
            self.otp_status.config(text=msg, fg=COLOR_RED)


    # ═════════════════════════════════════════════════════════════
    # SCREEN 3 – PATIENT INFO SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_patient_info_screen(self):
        self.clear()
        self.make_header("Patient Information")

        tk.Label(
            self.root,
            text    = "Please confirm / enter your details",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=10)

        form = tk.Frame(self.root, bg=COLOR_WHITE)
        form.pack(pady=5)

        # Name
        tk.Label(form, text="Full Name :",
                 font=FONT_NORMAL, bg=COLOR_WHITE,
                 anchor="e", width=14).grid(row=0, column=0, pady=6, padx=5)
        self.name_var = tk.StringVar(
            value=self.session.get("name", ""))
        tk.Entry(form, textvariable=self.name_var,
                 font=FONT_NORMAL, width=22,
                 relief=tk.GROOVE, bd=2).grid(row=0, column=1, pady=6)

        # Age
        tk.Label(form, text="Age :",
                 font=FONT_NORMAL, bg=COLOR_WHITE,
                 anchor="e", width=14).grid(row=1, column=0, pady=6, padx=5)
        self.age_var = tk.StringVar(
            value=str(self.session.get("age", "")))
        tk.Entry(form, textvariable=self.age_var,
                 font=FONT_NORMAL, width=22,
                 relief=tk.GROOVE, bd=2).grid(row=1, column=1, pady=6)

        # Gender
        tk.Label(form, text="Gender :",
                 font=FONT_NORMAL, bg=COLOR_WHITE,
                 anchor="e", width=14).grid(row=2, column=0, pady=6, padx=5)
        self.gender_var = tk.StringVar(
            value=self.session.get("gender", "Male"))
        gender_menu = tk.OptionMenu(
            form, self.gender_var, "Male", "Female", "Other")
        gender_menu.config(font=FONT_NORMAL, width=19,
                           bg=COLOR_WHITE, relief=tk.GROOVE)
        gender_menu.grid(row=2, column=1, pady=6)

        # Visit Type
        tk.Label(form, text="Visit Type :",
                 font=FONT_NORMAL, bg=COLOR_WHITE,
                 anchor="e", width=14).grid(row=3, column=0, pady=6, padx=5)
        self.visit_var = tk.StringVar(value="Outpatient (OPD)")
        visit_menu = tk.OptionMenu(
            form, self.visit_var,
            "Outpatient (OPD)", "Re-checkup", "Emergency")
        visit_menu.config(font=FONT_NORMAL, width=19,
                          bg=COLOR_WHITE, relief=tk.GROOVE)
        visit_menu.grid(row=3, column=1, pady=6)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=12)

        self.make_button(
            btn_frame,
            text    = "Next →",
            command = self.save_patient_info,
            color   = COLOR_BLUE,
        ).grid(row=0, column=0, padx=10)

        self.make_button(
            btn_frame,
            text    = "← Back",
            command = self.show_welcome,
            color   = COLOR_DARK,
        ).grid(row=0, column=1, padx=10)

        self.make_footer()


    # ─────────────────────────────────────────────────────────────

    def save_patient_info(self):
        name = self.name_var.get().strip()
        age  = self.age_var.get().strip()

        if not name:
            messagebox.showwarning("Required", "Please enter patient name.")
            return
        if not age.isdigit() or not (0 < int(age) < 130):
            messagebox.showwarning("Invalid", "Please enter a valid age.")
            return

        self.session["name"]       = name
        self.session["age"]        = int(age)
        self.session["gender"]     = self.gender_var.get()
        self.session["visit_type"] = self.visit_var.get()
        beep(1)
        self.show_symptom_screen()


    # ═════════════════════════════════════════════════════════════
    # SCREEN 4 – SYMPTOM SELECTION SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_symptom_screen(self):
        self.clear()
        self.make_header("Select Symptoms")

        tk.Label(
            self.root,
            text    = "Please select all applicable symptoms",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=8)

        # Symptom checkboxes
        self.symptom_vars = {}
        check_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        check_frame.pack(pady=5)

        symptoms = list(SYMPTOM_LABELS.items())
        cols     = 3

        for idx, (code, label) in enumerate(symptoms):
            row = idx // cols
            col = idx %  cols
            var = tk.BooleanVar()
            self.symptom_vars[code] = var
            tk.Checkbutton(
                check_frame,
                text     = f"  {label}",
                variable = var,
                font     = FONT_NORMAL,
                bg       = COLOR_WHITE,
                fg       = COLOR_DARK,
                selectcolor = COLOR_LIGHT,
                anchor   = "w",
                width    = 20,
            ).grid(row=row, column=col, sticky="w", padx=5, pady=3)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=8)

        self.make_button(
            btn_frame,
            text    = "Next – Health Check →",
            command = self.save_symptoms_go_health,
            color   = COLOR_BLUE,
            width   = 22,
        ).grid(row=0, column=0, padx=10)

        self.make_button(
            btn_frame,
            text    = "← Back",
            command = self.show_patient_info_screen,
            color   = COLOR_DARK,
        ).grid(row=0, column=1, padx=10)

        self.make_footer("Select all that apply – you can select multiple")


    # ─────────────────────────────────────────────────────────────

    def save_symptoms_go_health(self):
        selected = [
            code for code, var in self.symptom_vars.items()
            if var.get()
        ]
        self.session["symptoms"] = selected
        beep(1)
        self.show_health_screen()


    # ═════════════════════════════════════════════════════════════
    # SCREEN 5 – HEALTH MEASUREMENT SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_health_screen(self):
        self.clear()
        self.make_header("Health Parameter Measurement")

        tk.Label(
            self.root,
            text    = "Please follow the instructions below",
            font    = FONT_HEADING,
            bg      = COLOR_WHITE,
            fg      = COLOR_DARK,
        ).pack(pady=8)

        # Measurement display cards
        card_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        card_frame.pack(pady=5)

        # Temperature card
        temp_card = tk.Frame(
            card_frame, bg=COLOR_LIGHT,
            relief=tk.GROOVE, bd=2,
            padx=20, pady=10,
        )
        temp_card.grid(row=0, column=0, padx=15)

        tk.Label(temp_card, text="🌡  Body Temperature",
                 font=FONT_HEADING, bg=COLOR_LIGHT,
                 fg=COLOR_DARK).pack()
        self.temp_var = tk.StringVar(value="Measuring...")
        tk.Label(temp_card, textvariable=self.temp_var,
                 font=("Arial", 22, "bold"),
                 bg=COLOR_LIGHT, fg=COLOR_BLUE).pack(pady=5)
        tk.Label(temp_card,
                 text="Hold forehead near IR sensor",
                 font=FONT_SMALL, bg=COLOR_LIGHT,
                 fg="grey").pack()

        # Heart Rate card
        hr_card = tk.Frame(
            card_frame, bg=COLOR_LIGHT,
            relief=tk.GROOVE, bd=2,
            padx=20, pady=10,
        )
        hr_card.grid(row=0, column=1, padx=15)

        tk.Label(hr_card, text="❤  Heart Rate",
                 font=FONT_HEADING, bg=COLOR_LIGHT,
                 fg=COLOR_DARK).pack()
        self.hr_var = tk.StringVar(value="Measuring...")
        tk.Label(hr_card, textvariable=self.hr_var,
                 font=("Arial", 22, "bold"),
                 bg=COLOR_LIGHT, fg=COLOR_BLUE).pack(pady=5)
        tk.Label(hr_card,
                 text="Place finger on pulse sensor",
                 font=FONT_SMALL, bg=COLOR_LIGHT,
                 fg="grey").pack()

        # Environment card
        env_card = tk.Frame(
            self.root, bg=COLOR_LIGHT,
            relief=tk.GROOVE, bd=2,
            padx=20, pady=6,
        )
        env_card.pack(pady=8, fill=tk.X, padx=40)

        tk.Label(env_card, text="🌤  Environment",
                 font=FONT_HEADING, bg=COLOR_LIGHT,
                 fg=COLOR_DARK).pack(side=tk.LEFT, padx=10)
        self.env_var = tk.StringVar(value="Reading...")
        tk.Label(env_card, textvariable=self.env_var,
                 font=FONT_NORMAL,
                 bg=COLOR_LIGHT, fg=COLOR_DARK).pack(side=tk.LEFT)

        # Progress status
        self.health_status = tk.Label(
            self.root,
            text    = "⏳  Starting measurements...",
            font    = FONT_NORMAL,
            bg      = COLOR_WHITE,
            fg      = COLOR_BLUE,
        )
        self.health_status.pack(pady=5)

        self.make_footer("Please remain still during measurement")

        # Start measurement in background thread
        threading.Thread(
            target  = self.run_measurements,
            daemon  = True,
        ).start()


    # ─────────────────────────────────────────────────────────────

    def run_measurements(self):
        """Runs all sensor readings in a background thread."""

        # 1. Temperature
        self.root.after(0, lambda: self.health_status.config(
            text="🌡  Measuring body temperature..."))
        temp = read_temperature()
        self.root.after(0, lambda: self.temp_var.set(
            f"{temp} °C" if temp else "Error"))

        # 2. Heart Rate
        self.root.after(0, lambda: self.health_status.config(
            text="❤  Measuring heart rate – keep finger still..."))
        hr = read_heart_rate()
        self.root.after(0, lambda: self.hr_var.set(
            f"{hr} BPM" if hr else "Error"))

        # 3. Environment
        self.root.after(0, lambda: self.health_status.config(
            text="🌤  Reading environment..."))
        env = read_environment()
        self.root.after(0, lambda: self.env_var.set(
            f"Temp: {env['amb_temp']}°C  |  "
            f"Humidity: {env['humidity']}%  |  "
            f"Pressure: {env['pressure']} hPa"
        ))

        # Save to session
        self.session["temperature"] = temp
        self.session["heart_rate"]  = hr
        self.session["env"]         = env

        # 4. Department allocation
        dept, doctor, is_emg = allocate_department(
            self.session.get("symptoms", []), temp, hr
        )
        self.session["department"]   = dept
        self.session["doctor_type"]  = doctor
        self.session["is_emergency"] = is_emg

        # Done – go to token screen
        self.root.after(0, lambda: self.health_status.config(
            text="✅  Measurements complete!",
            fg=COLOR_GREEN,
        ))
        beep(2)

        # Auto-navigate after 1.5 seconds
        self.root.after(1500, self.show_token_screen)


    # ═════════════════════════════════════════════════════════════
    # SCREEN 6 – TOKEN & SUMMARY SCREEN
    # ═════════════════════════════════════════════════════════════

    def show_token_screen(self):
        self.clear()

        # Emergency or normal header
        if self.session.get("is_emergency"):
            self.make_header("🚨  EMERGENCY – Please See Staff Immediately")
        else:
            self.make_header("✅  Registration Complete")

        # Save everything to database
        result = save_full_registration(self.session)
        token  = result["token_number"]

        # ── Token Card ────────────────────────────────────────────
        card = tk.Frame(
            self.root,
            bg      = COLOR_LIGHT if not self.session.get("is_emergency")
                      else "#FADBD8",
            relief  = tk.GROOVE,
            bd      = 2,
            padx    = 20,
            pady    = 12,
        )
        card.pack(pady=8, fill=tk.X, padx=30)

        # Token number (large)
        tk.Label(
            card,
            text    = f"TOKEN: {token}",
            font    = ("Arial", 20, "bold"),
            bg      = card["bg"],
            fg      = COLOR_RED if self.session.get("is_emergency")
                      else COLOR_DARK,
        ).grid(row=0, column=0, columnspan=2, pady=4)

        # Details grid
        details = [
            ("Patient Name",  self.session.get("name", "--")),
            ("Age / Gender",
             f"{self.session.get('age','--')} yrs  |  "
             f"{self.session.get('gender','--')}"),
            ("Department",    self.session.get("department", "--")),
            ("Doctor Type",   self.session.get("doctor_type", "--")),
            ("Temperature",
             f"{self.session.get('temperature', '--')} °C"),
            ("Heart Rate",
             f"{self.session.get('heart_rate', '--')} BPM"),
            ("Visit Type",    self.session.get("visit_type", "--")),
            ("Date & Time",
             datetime.datetime.now().strftime("%d-%m-%Y  %H:%M")),
        ]

        for i, (label, value) in enumerate(details):
            tk.Label(
                card,
                text    = f"{label} :",
                font    = ("Arial", 11, "bold"),
                bg      = card["bg"],
                fg      = COLOR_DARK,
                anchor  = "e",
                width   = 16,
            ).grid(row=i+1, column=0, sticky="e", pady=2)

            tk.Label(
                card,
                text    = value,
                font    = ("Arial", 11),
                bg      = card["bg"],
                fg      = "#1A1A1A",
                anchor  = "w",
                width   = 28,
            ).grid(row=i+1, column=1, sticky="w", pady=2, padx=8)

        # Emergency warning
        if self.session.get("is_emergency"):
            tk.Label(
                self.root,
                text    = "⚠  CRITICAL VALUES DETECTED – Please inform hospital staff immediately!",
                font    = ("Arial", 11, "bold"),
                bg      = COLOR_WHITE,
                fg      = COLOR_RED,
                wraplength = 700,
            ).pack(pady=4)

        beep(3)

        # ── Bottom Buttons ────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        btn_frame.pack(pady=6)

        self.make_button(
            btn_frame,
            text    = "🔄  New Registration",
            command = self.show_welcome,
            color   = COLOR_DARK,
            width   = 20,
        ).grid(row=0, column=0, padx=15)

        self.make_button(
            btn_frame,
            text    = "🖨  Print Token",
            command = self.print_token,
            color   = COLOR_BLUE,
            width   = 20,
        ).grid(row=0, column=1, padx=15)

        self.make_footer(
            f"Thank you, {self.session.get('name','Patient')}! "
            f"Please proceed to {self.session.get('department','the department')}."
        )


    # ─────────────────────────────────────────────────────────────
    # PRINT TOKEN (basic console print / thermal printer)
    # ─────────────────────────────────────────────────────────────

    def print_token(self):
        """
        Prints the token summary.
        Currently prints to console.
        For thermal printer: add ESC/POS commands here.
        """
        print("\n" + "="*45)
        print(f"  {HOSPITAL_NAME}")
        print(f"  {HOSPITAL_CITY}")
        print("="*45)
        print(f"  TOKEN      : {self.session.get('token_number','--')}")
        print(f"  NAME       : {self.session.get('name','--')}")
        print(f"  AGE/GENDER : {self.session.get('age','--')} / "
              f"{self.session.get('gender','--')}")
        print(f"  DEPARTMENT : {self.session.get('department','--')}")
        print(f"  DOCTOR     : {self.session.get('doctor_type','--')}")
        print(f"  TEMP       : {self.session.get('temperature','--')} °C")
        print(f"  HEART RATE : {self.session.get('heart_rate','--')} BPM")
        print(f"  TIME       : "
              f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}")
        print("="*45 + "\n")
        messagebox.showinfo("Print", "Token sent to printer!\n"
                                     "(Check console in Mock Mode)")


# ═════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app  = HospitalKioskApp(root)
        root.mainloop()
    finally:
        cleanup()   # Release GPIO on exit
        print("[APP] Application closed.")