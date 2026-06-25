# ─────────────────────────────────────────────────────────────────
# sensors.py
# Project  : Automated Hospital Patient Registration System
# College  : Hindusthan College of Engineering and Technology
# Dept     : Electrical and Electronics Engineering
# Guide    : Dr. R. Rajeshkanna
# ─────────────────────────────────────────────────────────────────

import time
import random
from .config import (
    MOCK_MODE,
    BUZZER_PIN, TOUCH_PIN, PULSE_PIN,
    MLX90614_ADDR, BME280_ADDR,
    TEMP_HIGH, HR_LOW, HR_HIGH
)

# ── Only import hardware libraries if NOT in mock mode ───────────
if not MOCK_MODE:
    import smbus2  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    # GPIO Setup
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
    In mock mode – prints a beep message instead.
    """
    if MOCK_MODE:
        print(f"[BUZZER] Beep x{times}")
        return

    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.1)


# ─────────────────────────────────────────────────────────────────
# MLX90614 – IR BODY TEMPERATURE SENSOR
# ─────────────────────────────────────────────────────────────────

def read_temperature():
    """
    Reads body temperature using MLX90614 IR sensor via I2C.
    Mock mode returns a realistic random value between 36.0 – 39.5 °C.
    Returns: float – temperature in Celsius
    """
    if MOCK_MODE:
        # Simulate a realistic body temperature
        temp = round(random.uniform(36.0, 39.5), 1)
        print(f"[MOCK] Temperature: {temp} °C")
        time.sleep(2)   # simulate measurement delay
        return temp

    # ── Real Hardware Code ────────────────────────────────────────
    try:
        bus  = smbus2.SMBus(1)
        # Read 3 bytes from register 0x07 (object temperature)
        data = bus.read_i2c_block_data(MLX90614_ADDR, 0x07, 3)
        raw  = (data[1] << 8) | data[0]
        temp = round(raw * 0.02 - 273.15, 1)
        bus.close()
        return temp
    except Exception as e:
        print(f"[ERROR] Temperature sensor: {e}")
        return None


# ─────────────────────────────────────────────────────────────────
# KY-039 – PULSE / HEART RATE SENSOR
# ─────────────────────────────────────────────────────────────────

def read_heart_rate():
    """
    Reads heart rate using KY-039 pulse sensor via GPIO.
    Counts pulses over 15 seconds and extrapolates to BPM.
    Mock mode returns a realistic random value between 60 – 110 BPM.
    Returns: int – heart rate in BPM
    """
    if MOCK_MODE:
        # Simulate a realistic heart rate
        hr = random.randint(60, 110)
        print(f"[MOCK] Heart Rate: {hr} BPM")
        time.sleep(3)   # simulate measurement delay
        return hr

    # ── Real Hardware Code ────────────────────────────────────────
    try:
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
            time.sleep(0.001)   # 1ms sampling interval

        # Extrapolate 15s count to 60s (BPM)
        bpm = pulse_count * 4
        return bpm
    except Exception as e:
        print(f"[ERROR] Pulse sensor: {e}")
        return None


# ─────────────────────────────────────────────────────────────────
# BME280 – ENVIRONMENTAL SENSOR
# ─────────────────────────────────────────────────────────────────

def read_environment():
    """
    Reads ambient temperature, humidity, and pressure using BME280.
    Mock mode returns realistic random values.
    Returns: dict with keys – amb_temp, humidity, pressure
    """
    if MOCK_MODE:
        env = {
            "amb_temp" : round(random.uniform(24.0, 32.0), 1),
            "humidity" : round(random.uniform(40.0, 75.0), 1),
            "pressure" : round(random.uniform(1005.0, 1015.0), 1),
        }
        print(f"[MOCK] Environment: {env}")
        time.sleep(1)   # simulate measurement delay
        return env

    # ── Real Hardware Code ────────────────────────────────────────
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
        return env
    except Exception as e:
        print(f"[ERROR] BME280 sensor: {e}")
        return {"amb_temp": None, "humidity": None, "pressure": None}


# ─────────────────────────────────────────────────────────────────
# TRIAGE LOGIC – Department Allocation
# ─────────────────────────────────────────────────────────────────

def allocate_department(symptoms, temperature, heart_rate):
    """
    Determines the appropriate medical department based on:
    - Selected symptoms
    - Measured body temperature
    - Measured heart rate

    Returns: tuple (department: str, doctor_type: str, is_emergency: bool)
    """
    from .config import SYMPTOM_DEPT_MAP

    # ── Critical Alert Check (Emergency) ─────────────────────────
    is_emergency = False
    if temperature and (temperature > TEMP_HIGH):
        is_emergency = True
    if heart_rate and (heart_rate < HR_LOW or heart_rate > HR_HIGH):
        is_emergency = True

    if is_emergency:
        return "Emergency", "Emergency Physician", True

    # ── Symptom-Based Scoring ─────────────────────────────────────
    scores = {}
    for symptom in symptoms:
        dept = SYMPTOM_DEPT_MAP.get(symptom, "General Medicine")
        scores[dept] = scores.get(dept, 0) + 1

    if not scores:
        return "General Medicine", "General Practitioner", False

    # Department with highest symptom score wins
    best_dept   = max(scores, key=scores.get)
    doctor_type = (
        "General Practitioner"
        if best_dept == "General Medicine"
        else "Specialist"
    )
    return best_dept, doctor_type, False


# ─────────────────────────────────────────────────────────────────
# GPIO CLEANUP (call on app exit)
# ─────────────────────────────────────────────────────────────────

def cleanup():
    """
    Releases GPIO resources on Raspberry Pi.
    Safe to call in mock mode too.
    """
    if not MOCK_MODE:
        try:
            GPIO.cleanup()
            print("[GPIO] Cleanup done.")
        except Exception as e:
            print(f"[ERROR] GPIO cleanup: {e}")