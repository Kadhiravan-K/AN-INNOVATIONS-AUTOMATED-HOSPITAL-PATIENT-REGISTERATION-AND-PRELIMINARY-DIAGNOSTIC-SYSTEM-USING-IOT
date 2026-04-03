# ─────────────────────────────────────────────────────────────────
# sensors/pulse.py — KY-039 Pulse / Heart Rate Sensor
# ─────────────────────────────────────────────────────────────────

import time
import random
from config import MOCK_MODE, PULSE_PIN
from utils.logger import get_logger

log = get_logger("sensor.pulse")


def read_heart_rate():
    """
    Reads heart rate using KY-039 pulse sensor via GPIO.
    Counts pulses over 15 seconds and extrapolates to BPM.
    Mock mode returns a realistic random value between 60 – 110 BPM.

    Returns:
        int — heart rate in BPM, or None on error
    """
    if MOCK_MODE:
        hr = random.randint(60, 110)
        log.info("MOCK Heart Rate: %d BPM", hr)
        time.sleep(3)  # simulate measurement delay
        return hr

    # ── Real Hardware ─────────────────────────────────────────────
    try:
        import RPi.GPIO as GPIO  # type: ignore

        pulse_count = 0
        start_time  = time.time()
        last_state  = GPIO.input(PULSE_PIN)

        # Sample for 15 seconds
        while time.time() - start_time < 15:
            current_state = GPIO.input(PULSE_PIN)
            # Detect rising edge (LOW → HIGH transition = 1 pulse)
            if current_state != last_state and current_state == GPIO.HIGH:
                pulse_count += 1
            last_state = current_state
            time.sleep(0.001)  # 1ms sampling interval

        # Extrapolate 15s count to 60s (BPM)
        bpm = pulse_count * 4
        log.info("Heart Rate: %d BPM", bpm)
        return bpm

    except Exception as e:
        log.error("Pulse sensor error: %s", e)
        return None
