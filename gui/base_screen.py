# ─────────────────────────────────────────────────────────────────
# gui/base_screen.py — Shared CTk UI helpers for all screens
# ─────────────────────────────────────────────────────────────────

import customtkinter as ctk
from config import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_SURFACE,
    COLOR_CARD, COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_SUCCESS,
    COLOR_WARNING, COLOR_DANGER, COLOR_BORDER,
    FONT_TITLE, FONT_HEADING, FONT_NORMAL, FONT_SMALL, FONT_TINY,
    FONT_LARGE, FONT_ICON,
    HOSPITAL_NAME, HOSPITAL_CITY,
    WINDOW_WIDTH, WINDOW_HEIGHT,
)
from services.i18n import i18n


class BaseScreen:
    """
    Base class providing shared UI helpers for all CustomTkinter screens.
    """

    def __init__(self, app):
        self.app  = app
        self.root = app.root

    def clear(self):
        """Remove all widgets and cleanup."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def translate(self, key, default=None):
        """Helper to get translated text."""
        return i18n.get(key, default)

    def make_header(self, title):
        """Create a modern solid header with hospital name and screen title."""
        header_height = 80
        header = ctk.CTkFrame(
            master=self.root, 
            width=WINDOW_WIDTH, 
            height=header_height, 
            fg_color=COLOR_PRIMARY,
            corner_radius=0
        )
        header.pack(fill="x", side="top")

        # Hospital name (small, top)
        ctk.CTkLabel(
            master=header,
            text=HOSPITAL_NAME,
            font=FONT_TINY,
            text_color="#A8DADC",
        ).pack(pady=(10, 0))

        # Screen title (large, center)
        ctk.CTkLabel(
            master=header,
            text=title,
            font=FONT_TITLE,
            text_color="#FFFFFF",
        ).pack(pady=(0, 10))

        # Accent line at bottom
        accent = ctk.CTkFrame(
            master=self.root, 
            height=3, 
            fg_color=COLOR_ACCENT, 
            corner_radius=0
        )
        accent.pack(fill="x", side="top")

        return header

    def make_footer(self, text=""):
        """Create a slim footer bar."""
        footer = ctk.CTkFrame(
            master=self.root, 
            height=35, 
            fg_color=COLOR_PRIMARY, 
            corner_radius=0
        )
        footer.pack(fill="x", side="bottom")

        ctk.CTkLabel(
            master=footer,
            text=text or HOSPITAL_CITY,
            font=FONT_TINY,
            text_color="#A8DADC",
        ).pack(pady=5, expand=True)

        return footer

    def make_button(self, parent, text, command, color=None, width=150, height=40, font=None, textvariable=None):
        """Create a styled CTkButton with rounded corners and hover effects."""
        bg_color = color or COLOR_ACCENT
        btn = ctk.CTkButton(
            master=parent,
            text=text,
            command=command,
            font=font or FONT_HEADING,
            fg_color=bg_color,
            hover_color=self._darken(bg_color, 0.15),
            text_color="#FFFFFF",
            width=width,
            height=height,
            corner_radius=8,
            cursor="hand2",
            textvariable=textvariable
        )
        return btn

    def make_card(self, parent, padx=20, pady=12, bg=None):
        """Create a modern card-style frame giving a 3D-like elevated feel."""
        bg = bg or COLOR_CARD
        
        card = ctk.CTkFrame(
            master=parent,
            fg_color=bg,
            corner_radius=20,  # Increased for modern look
            border_width=2,
            border_color=COLOR_BORDER
        )
        return card, card

    def make_status_label(self, parent, text=""):
        """Create a status label for messages / errors."""
        label = ctk.CTkLabel(
            master=parent,
            text=text,
            font=FONT_SMALL,
            text_color=COLOR_TEXT_LIGHT,
        )
        return label

    def make_entry(self, parent, textvariable=None, width=200, show="", font=None, justify="center"):
        """Create a modern styled text entry."""
        entry = ctk.CTkEntry(
            master=parent,
            textvariable=textvariable,
            font=font or ("Segoe UI", 16),
            width=width,
            height=40,
            show=show,
            justify=justify,
            fg_color="#FFFFFF",
            text_color=COLOR_TEXT,
            border_color=COLOR_BORDER,
            border_width=2,
            corner_radius=8,
        )
        # Focus border color can be handled in theme or directly when supported
        return entry

    def make_progress_bar(self, parent, width=400, height=10):
        """Create a modern progress bar using CTkProgressBar."""
        progress = ctk.CTkProgressBar(
            master=parent,
            width=width, 
            height=height,
            corner_radius=5,
            progress_color=COLOR_ACCENT,
            fg_color=COLOR_BORDER
        )
        progress.set(0)

        # we patch the method to match existing interface
        def update_progress(fraction):
            progress.set(min(max(fraction, 0), 1))
            if fraction >= 1.0:
                progress.configure(progress_color=COLOR_SUCCESS)
            elif fraction > 0.66:
                progress.configure(progress_color=COLOR_ACCENT)
        
        progress.update_progress = update_progress
        return progress

    # ─────────────────────────────────────────────────────────────
    # UTILITY – Hex color helpers
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def _darken(hex_color, factor=0.1):
        """Darken a hex color by a factor (0.0 to 1.0)."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"
