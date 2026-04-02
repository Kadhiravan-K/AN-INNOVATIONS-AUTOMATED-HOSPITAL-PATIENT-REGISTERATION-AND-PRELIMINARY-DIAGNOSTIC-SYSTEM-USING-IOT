# ─────────────────────────────────────────────────────────────────
# controllers/sensor_controller.py — Sensor orchestration
# ─────────────────────────────────────────────────────────────────

from sensors import read_temperature, read_heart_rate, read_environment
from sensors.spo2 import read_spo2
from utils.logger import get_logger

log = get_logger("controller.sensor")


class SensorController:
    """Wraps sensor readings with error handling and callbacks."""

    def __init__(self):
        self.temperature = None
        self.heart_rate  = None
        self.environment = None
        self.spo2        = None

    def get_temperature(self):
        """Read body temperature from MLX90614."""
        self.temperature = read_temperature()
        return self.temperature

    def get_heart_rate(self):
        """Read heart rate from KY-039."""
        self.heart_rate = read_heart_rate()
        return self.heart_rate

    def get_environment(self):
        """Read environment from BME280."""
        self.environment = read_environment()
        return self.environment

    def get_spo2(self):
        """Read SpO2 from MAX30102."""
        self.spo2 = read_spo2()
        return self.spo2

    def measure_all(self):
        """
        Perform all measurements sequentially.
        Returns: dict with temperature, heart_rate, env, spo2
        """
        self.get_temperature()
        self.get_heart_rate()
        self.get_spo2() # Include SpO2 in measurement flow
        self.get_environment()

        log.info(
            "All measurements done. Temp=%.1f, HR=%s, SpO2=%s",
            self.temperature or 0,
            self.heart_rate or 0,
            self.spo2 or 0,
        )

        return {
            "temperature": self.temperature,
            "heart_rate" : self.heart_rate,
            "env"        : self.environment or {},
            "spo2"       : self.spo2,
        }
