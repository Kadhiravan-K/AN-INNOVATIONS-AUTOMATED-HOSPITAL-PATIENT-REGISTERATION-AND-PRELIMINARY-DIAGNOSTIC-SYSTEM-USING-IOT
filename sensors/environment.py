# ─────────────────────────────────────────────────────────────────
# sensors/environment.py — BME280 + Buzzer + GPIO Cleanup
# ─────────────────────────────────────────────────────────────────

import time
import random
from config import MOCK_MODE, BUZZER_PIN, TOUCH_PIN, PULSE_PIN, BME280_ADDR
from utils.logger import get_logger

log = get_logger("sensor.env")

# ── Hardware init (only on real Raspberry Pi) ────────────────────
if not MOCK_MODE:
    import smbus2  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(TOUCH_PIN,  GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PULSE_PIN,  GPIO.IN)


# ─────────────────────────────────────────────────────────────────
# BUZZER
# ─────────────────────────────────────────────────────────────────

def beep(times=1, duration=0.15):
    """
    Beep the buzzer a given number of times.
    In mock mode — prints a beep message instead.
    """
    if MOCK_MODE:
        log.debug("BUZZER beep x%d", times)
        return

    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.1)


# ─────────────────────────────────────────────────────────────────
# BME280 – ENVIRONMENTAL SENSOR
# ─────────────────────────────────────────────────────────────────

def read_environment():
    """
    Reads ambient temperature, humidity, and pressure using BME280.
    Mock mode returns realistic random values.

    Returns:
        dict with keys — amb_temp, humidity, pressure
    """
    if MOCK_MODE:
        env = {
            "amb_temp" : round(random.uniform(24.0, 32.0), 1),
            "humidity" : round(random.uniform(40.0, 75.0), 1),
            "pressure" : round(random.uniform(1005.0, 1015.0), 1),
        }
        log.info("MOCK Environment: %s", env)
        time.sleep(1)
        return env

    # ── Real Hardware ─────────────────────────────────────────────
    try:
        import adafruit_bme280  # type: ignore
        import board  # type: ignore
        import busio  # type: ignore

        i2c    = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bme280.Adafruit_BME280_I2C(
                     i2c, address=BME280_ADDR
                 )
        env = {
            "amb_temp" : round(sensor.temperature, 1),
            "humidity" : round(sensor.humidity, 1),
            "pressure" : round(sensor.pressure, 1),
        }
        log.info("Environment: %s", env)
        return env

    except Exception as e:
        log.error("BME280 sensor error: %s", e)
        return {"amb_temp": None, "humidity": None, "pressure": None}


# ─────────────────────────────────────────────────────────────────
# GPIO CLEANUP
# ─────────────────────────────────────────────────────────────────

def cleanup():
    """
    Releases GPIO resources on Raspberry Pi.
    Safe to call in mock mode too.
    """
    if not MOCK_MODE:
        try:
            GPIO.cleanup()
            log.info("GPIO cleanup done.")
        except Exception as e:
            log.error("GPIO cleanup error: %s", e)
