# ─────────────────────────────────────────────────────────────────
# utils/token_generator.py — Unique token number generation
# ─────────────────────────────────────────────────────────────────

import datetime
import random


def generate_token_number():
    """
    Generates a unique token number.
    Format: YYYYMMDD-XXXX  (e.g. 20260328-4721)
    """
    date_part   = datetime.datetime.now().strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"{date_part}-{random_part}"
