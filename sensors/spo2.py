# ─────────────────────────────────────────────────────────────────
# sensors/spo2.py — SpO2 & Heart Rate (MAX30102)
# ─────────────────────────────────────────────────────────────────

import time
import random
from config import MOCK_MODE
from utils.logger import get_logger

log = get_logger("sensors.spo2")

def read_spo2():
    """
    Reads Oxygen Saturation (SpO2) from MAX30102.
    Returns: int (90-100) or None if error.
    """
    if MOCK_MODE:
        time.sleep(1.5) # Simulate sensing
        val = random.randint(94, 99)
        log.info(f"MOCK SpO2: {val}%")
        return val

    try:
        # Real implementation would use something like `max30102` library
        # from max30102 import MAX30102
        # sensor = MAX30102()
        # return sensor.read_spo2()
        log.warning("Real MAX30102 not implemented – using fallback mock.")
        return random.randint(95, 99)
    except Exception as e:
        log.error(f"SpO2 sensor error: {e}")
        return None
