# Automated Hospital Patient Registration System

An intelligent IoT-based hospital patient registration kiosk system built with Python and Tkinter.

---

## 📁 Project Structure

```
hospital_registration/
├── main.py                          ← Entry point (~85 lines)
├── config.py                        ← All settings & configuration
├── requirements.txt
├── README.md
│
├── gui/                             ← UI Screens
│   ├── __init__.py
│   ├── base_screen.py               ← Shared UI helpers (gradient headers, cards)
│   ├── welcome_screen.py            ← Registration type selection
│   ├── aadhaar_screen.py            ← Aadhaar entry + OTP verification
│   ├── patient_info_screen.py       ← Patient details form
│   ├── symptom_screen.py            ← Symptom selection (categorized cards)
│   ├── health_screen.py             ← Animated health measurement
│   └── token_screen.py              ← Final token + summary
│
├── controllers/                     ← Business logic orchestration
│   ├── __init__.py
│   ├── registration_controller.py   ← Session state & flow manager
│   ├── sensor_controller.py         ← Sensor reading orchestration
│   └── auth_controller.py           ← Authentication wrapper
│
├── sensors/                         ← Hardware sensor modules
│   ├── __init__.py
│   ├── temperature.py               ← MLX90614 IR sensor
│   ├── pulse.py                     ← KY-039 heart rate sensor
│   └── environment.py               ← BME280 + buzzer + GPIO
│
├── auth/                            ← Identity verification
│   ├── __init__.py
│   └── aadhaar_auth.py              ← Aadhaar OTP send/verify
│
├── database/                        ← Data persistence
│   ├── __init__.py
│   ├── db_setup.py                  ← Table creation
│   ├── db_operations.py             ← CRUD operations
│   └── models.py                    ← Data classes
│
├── services/                        ← Core business services
│   ├── __init__.py
│   ├── health_analysis.py           ← Vital sign analysis
│   └── department_logic.py          ← Triage & department allocation
│
├── utils/                           ← Utilities
│   ├── __init__.py
│   ├── token_generator.py           ← Token number generation
│   ├── report_generator.py          ← Print report formatting
│   └── logger.py                    ← Centralized logging
│
├── assets/                          ← Static assets
│   ├── images/
│   └── icons/
│
└── DOCS/
    └── PROVISIONAL_SPECIFICATION.md
```

---

## 💻 How to Run on Laptop (Mock Mode)

### Step 1 – Install Python

Download Python 3.9 or above from:
https://www.python.org/downloads/

### Step 2 – Install Dependencies

```
pip install -r requirements.txt
```

### Step 3 – Make sure Mock Mode is ON

Open `config.py` and check:

```python
MOCK_MODE = True   # must be True for laptop
```

### Step 4 – Run the App

```
python main.py
```

### Step 5 – Test OTP

- Enter any 12-digit number (e.g. 234567891234)
- Check your terminal/console window
- You will see the MOCK OTP in the logs
- Enter that OTP in the app

---

## 🔌 How to Run on Raspberry Pi (Real Hardware)

### Step 1 – Enable I2C on Raspberry Pi

```
sudo raspi-config
→ Interface Options → I2C → Enable
```

### Step 2 – Install Dependencies

```
pip install -r requirements.txt
pip install RPi.GPIO smbus2
pip install adafruit-circuitpython-bme280
```

### Step 3 – Switch to Real Mode

Open `config.py` and change:

```python
MOCK_MODE  = False   # change to False
FULLSCREEN = True    # set True for kiosk mode
```

### Step 4 – Wire the Components

| Component    | Raspberry Pi Pin        |
| ------------ | ----------------------- |
| MLX90614 SDA | GPIO 2 (Pin 3)          |
| MLX90614 SCL | GPIO 3 (Pin 5)          |
| BME280 SDA   | GPIO 2 (Pin 3) – shared |
| BME280 SCL   | GPIO 3 (Pin 5) – shared |
| KY-039 OUT   | GPIO 17 (Pin 11)        |
| TTP223 OUT   | GPIO 18 (Pin 12)        |
| Buzzer +     | GPIO 27 (Pin 13)        |
| All GND      | GND (Pin 6)             |
| Sensors VCC  | 3.3V (Pin 1)            |

### Step 5 – Run the App

```
python main.py
```

---

## 🖥️ App Flow

```
Welcome Screen
    │
    ├── Permanent Registration
    │       │
    │       ├── Aadhaar Entry
    │       └── OTP Verification
    │               │
    │               ▼
    └── Temporary Registration
                │
                ▼
        Patient Info (Name/Age/Gender)
                │
                ▼
        Symptom Selection (Categorized)
                │
                ▼
        Health Measurement
        (Temperature + Heart Rate + Environment)
        with animated progress bar
                │
                ▼
        Token + Patient Summary
```

---

## ⚙️ Configuration (config.py)

| Setting    | Default         | Description                      |
| ---------- | --------------- | -------------------------------- |
| MOCK_MODE  | True            | True=Laptop / False=Raspberry Pi |
| FULLSCREEN | False           | True for kiosk deployment        |
| TEMP_HIGH  | 38.5°C          | Fever threshold for emergency    |
| HR_LOW     | 50 BPM          | Bradycardia threshold            |
| HR_HIGH    | 120 BPM         | Tachycardia threshold            |
| DB_PATH    | .db file        | SQLite database location         |
| LOG_FILE   | .log file       | Application log file             |

---

## 🗃️ Database Tables

| Table          | Stores                               |
| -------------- | ------------------------------------ |
| patients       | Name, age, gender, Aadhaar hash      |
| health_records | Temperature, heart rate, environment |
| symptoms       | Selected symptom codes               |
| tokens         | Token number, department, doctor     |

---

## 🚨 Emergency Detection

The system automatically redirects to **Emergency Department** if:

- Body temperature > **38.5°C**
- Heart rate < **50 BPM** (Bradycardia)
- Heart rate > **120 BPM** (Tachycardia)

---

## 📝 Notes

- Aadhaar number is **never stored** – only SHA-256 hash is saved
- Mock OTP is printed to **console logs** for testing
- Database file `hospital_kiosk.db` is auto-created on first run
- Application logs are saved to `hospital_kiosk.log`
- To reset database – simply delete the `.db` file and restart

---

## 🚀 Quick Start (3 steps)

1. Copy all files into one folder
2. `pip install requests`
3. `python main.py`
