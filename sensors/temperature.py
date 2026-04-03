# ─────────────────────────────────────────────────────────────────
# sensors/temperature.py — MLX90614 IR Body Temperature Sensor
# ─────────────────────────────────────────────────────────────────

import time
import random
from config import MOCK_MODE, MLX90614_ADDR
from utils.logger import get_logger

log = get_logger("sensor.temp")


def read_temperature():
    """
    Reads body temperature using MLX90614 IR sensor via I2C.
    Mock mode returns a realistic random value between 36.0 – 39.5 °C.

    Returns:
        float — temperature in Celsius, or None on error
    """
    if MOCK_MODE:
        temp = round(random.uniform(36.0, 39.5), 1)
        log.info("MOCK Temperature: %.1f °C", temp)
        time.sleep(2)  # simulate measurement delay
        return temp

    # ── Real Hardware ─────────────────────────────────────────────
    try:
        import smbus2  # type: ignore

        bus  = smbus2.SMBus(1)
        # Read 3 bytes from register 0x07 (object temperature)
        data = bus.read_i2c_block_data(MLX90614_ADDR, 0x07, 3)
        raw  = (data[1] << 8) | data[0]
        temp = round(raw * 0.02 - 273.15, 1)
        bus.close()

        log.info("Temperature: %.1f °C", temp)
        return temp

    except Exception as e:
        log.error("Temperature sensor error: %s", e)
        return None
