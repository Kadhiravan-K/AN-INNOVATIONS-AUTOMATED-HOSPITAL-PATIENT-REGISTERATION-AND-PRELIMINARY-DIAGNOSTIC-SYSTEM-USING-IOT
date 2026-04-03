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
    COLOR_PRIMARY, COLOR_GLASS
)
from sensors import beep

class PatientInfoScreen(BaseScreen):
    """Patient information form screen."""

    def show(self):
        self.clear()
        self.make_header(self.translate("patient_info_title"))
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
        self._make_field(form_card, self.translate("name_label"), 0)
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
        
        # Date of Birth (Popup Based Selection)
        self._make_field(form_card, self.translate("dob_label"), 1)
        
        self.day_var = ctk.StringVar(value="01")
        self.month_var = ctk.StringVar(value="Jan")
        self.year_var = ctk.StringVar(value="2000")
        self.dob_display_var = ctk.StringVar(value=self.translate("btn_select_date", "Select Date 📅"))

        self.dob_btn = self.make_button(
            form_card, text=self.translate("btn_select_date", "Select Date 📅"),
            command=self._show_dob_picker,
            color=COLOR_PRIMARY, width=250, height=40,
        )
        self.dob_btn.grid(row=1, column=1, pady=8, padx=10, sticky="w")

        # Gender
        self._make_field(form_card, self.translate("gender_label"), 2)
        gender_options = [self.translate("male"), self.translate("female"), self.translate("other")]
        self.gender_var = ctk.StringVar(value=gender_options[0])
        gender_menu = ctk.CTkOptionMenu(
            master=form_card,
            values=gender_options,
            variable=self.gender_var,
            font=FONT_NORMAL,
            width=250,
            fg_color=COLOR_CARD,
            button_color=COLOR_ACCENT,
            button_hover_color=self._darken(COLOR_ACCENT),
            text_color=COLOR_TEXT,
        )
        gender_menu.grid(row=2, column=1, pady=6, padx=10, sticky="w")

        # Visit Type
        self._make_field(form_card, self.translate("visit_label"), 3)
        visit_options = [self.translate("opd"), self.translate("emergency_visit")]
        self.visit_var = ctk.StringVar(value=visit_options[0])
        visit_menu = ctk.CTkOptionMenu(
            master=form_card,
            values=visit_options,
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
            btn_frame, text=self.translate("btn_back"),
            command=lambda: self.app.show_screen("welcome"),
            color=COLOR_TEXT_LIGHT, width=140,
        ).grid(row=0, column=0, padx=8)

        self.make_button(
            btn_frame, text=self.translate("btn_next"),
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

    def _show_dob_picker(self):
        """Open a popup window for date selection."""
        beep(1)
        picker = ctk.CTkToplevel(self.root)
        picker.title("Select Date of Birth")
        picker.geometry("350x250")
        picker.attributes("-topmost", True)
        picker.configure(fg_color=COLOR_SURFACE)

        # Center picker
        self.app.center_window(picker, 350, 250)

        ctk.CTkLabel(picker, text="Scroll to select your DOB", font=FONT_NORMAL, text_color=COLOR_TEXT).pack(pady=10)

        container = ctk.CTkFrame(picker, fg_color="transparent")
        container.pack(pady=5)

        # Shared variables for dynamic updates
        self.day_scroll = None
        self.day_btns = []
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        def is_leap_year(y):
            y = int(y)
            return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

        def get_max_days():
            m_idx = months.index(self.month_var.get())
            y = int(self.year_var.get())
            days_map = [31, 29 if is_leap_year(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return days_map[m_idx]

        def update_day_column():
            if not self.day_scroll: return
            # Target max days
            max_d = get_max_days()
            
            # Reset current day if it's out of bounds
            if int(self.day_var.get()) > max_d:
                self.day_var.set("01")

            # Redraw buttons
            for b in self.day_btns: b.destroy()
            self.day_btns.clear()

            for i in range(1, max_d + 1):
                v = f"{i:02d}"
                is_sel = (self.day_var.get() == v)
                b = ctk.CTkButton(self.day_scroll, text=v, width=50, height=28,
                                  fg_color=COLOR_PRIMARY if is_sel else "transparent",
                                  text_color="white" if is_sel else COLOR_TEXT,
                                  font=FONT_SMALL, command=lambda x=v: select_day(x))
                b.pack(pady=1)
                self.day_btns.append(b)

        def select_day(val):
            self.day_var.set(val)
            for i, b in enumerate(self.day_btns):
                is_sel = (val == f"{i+1:02d}")
                b.configure(fg_color=COLOR_PRIMARY if is_sel else "transparent",
                            text_color="white" if is_sel else COLOR_TEXT)

        def make_scroll_col(parent, values, var, width, callback=None):
            scroll = ctk.CTkScrollableFrame(parent, width=width, height=120, 
                                           fg_color=COLOR_CARD, corner_radius=8,
                                           scrollbar_button_color=COLOR_PRIMARY)
            scroll.pack(side="left", padx=5)
            btns = []
            def select(val, btn):
                var.set(val)
                for b in btns: b.configure(fg_color="transparent", text_color=COLOR_TEXT)
                btn.configure(fg_color=COLOR_PRIMARY, text_color="white")
                if callback: callback()

            for v in values:
                is_sel = (var.get() == v)
                b = ctk.CTkButton(scroll, text=v, width=width-10, height=28,
                                  fg_color=COLOR_PRIMARY if is_sel else "transparent",
                                  text_color="white" if is_sel else COLOR_TEXT,
                                  font=FONT_SMALL, command=lambda x=v: select(x, btns[values.index(x)]))
                b.pack(pady=1); btns.append(b)
            return scroll, btns

        # ── Day Column ──
        self.day_scroll = ctk.CTkScrollableFrame(container, width=60, height=120, 
                                                fg_color=COLOR_CARD, corner_radius=8,
                                                scrollbar_button_color=COLOR_PRIMARY)
        self.day_scroll.pack(side="left", padx=5)
        update_day_column()

        # ── Month Column ──
        make_scroll_col(container, months, self.month_var, 80, update_day_column)

        # ── Year Column ──
        years = [str(y) for y in range(datetime.datetime.now().year, 1919, -1)]
        make_scroll_col(container, years, self.year_var, 80, update_day_column)

        def confirm():
            new_date = f"{self.day_var.get()} / {self.month_var.get()} / {self.year_var.get()}"
            self.dob_display_var.set(new_date)
            self.dob_btn.configure(text=new_date) # Refresh button text
            picker.destroy()
            beep(1)

        # Set protocol for auto-save if closed via 'X'
        picker.protocol("WM_DELETE_WINDOW", confirm)

        self.make_button(picker, text="Save & Close", command=confirm, color=COLOR_PRIMARY, width=200).pack(pady=15)

    def _save_and_next(self):
        name = self.name_var.get().strip()
        if self.dob_display_var.get() == "Select Date 📅":
            messagebox.showwarning("Missing Info", "Please select your Date of Birth.")
            return

        month_map = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", 
                     "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
        dob_str = f"{self.day_var.get()}/{month_map[self.month_var.get()]}/{self.year_var.get()}"

        if not name:
            messagebox.showwarning("Required", "Please enter patient name.")
            return
            
        try:
            dob = datetime.datetime.strptime(dob_str, "%d/%m/%Y")
            today = datetime.datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0 or age > 120: raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid", "Please enter a valid Date of Birth.")
            return

        self.app.controller.save_patient_info(name, str(age), self.gender_var.get(), self.visit_var.get())
        beep(1); self.app.show_screen("symptoms")
