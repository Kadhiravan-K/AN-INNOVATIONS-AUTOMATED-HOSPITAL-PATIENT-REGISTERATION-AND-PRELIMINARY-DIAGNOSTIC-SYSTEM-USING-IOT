# Automated Hospital Patient Registration System
---

## 📁 Project Structure

```
hospital_registration/
├── main.py            ← Run this file to start the app
├── sensors.py         ← Sensor logic (MLX90614, KY-039, BME280)
├── database.py        ← SQLite database operations
├── auth.py            ← Aadhaar OTP authentication
├── config.py          ← All settings in one place
├── requirements.txt   ← Python packages
└── README.md          ← This file
```

---

## 💻 How to Run on Laptop (Mock Mode)

### Step 1 – Install Python

Download Python 3.9 or above from:
https://www.python.org/downloads/

### Step 2 – Create Project Folder

```
mkdir hospital_registration
cd hospital_registration
```

Copy all 6 files into this folder.

### Step 3 – Install Dependencies

```
pip install -r requirements.txt
```

### Step 4 – Make sure Mock Mode is ON

Open config.py and check:

```python
MOCK_MODE = True   ← must be True for laptop
```

### Step 5 – Run the App

```
python main.py
```

### Step 6 – Test OTP

- Enter any 12-digit number (e.g. 234567891234)
- Check your terminal/console window
- You will see: [MOCK OTP] Your OTP is: XXXXXX
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

Open config.py and change:

```python
MOCK_MODE  = False   ← change to False
FULLSCREEN = True    ← set True for kiosk mode
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
        Symptom Selection
                │
                ▼
        Health Measurement
        (Temperature + Heart Rate + Environment)
                │
                ▼
        Token + Patient Summary
```

---

## ⚙️ Configuration (config.py)

| Setting    | Default  | Description                      |
| ---------- | -------- | -------------------------------- |
| MOCK_MODE  | True     | True=Laptop / False=Raspberry Pi |
| FULLSCREEN | False    | True for kiosk deployment        |
| TEMP_HIGH  | 38.5°C   | Fever threshold for emergency    |
| HR_LOW     | 50 BPM   | Bradycardia threshold            |
| HR_HIGH    | 120 BPM  | Tachycardia threshold            |
| DB_PATH    | .db file | SQLite database location         |

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
- Mock OTP is printed to **terminal/console** for testing
- Database file `hospital_kiosk.db` is auto-created on first run
- To reset database – simply delete the `.db` file and restart

```

---

## ✅ ALL 6 FILES COMPLETE! 🎉

Here's your complete file checklist:

| # | File | Status |
|---|---|---|
| 1 | `config.py` | ✅ Done |
| 2 | `sensors.py` | ✅ Done |
| 3 | `database.py` | ✅ Done |
| 4 | `auth.py` | ✅ Done |
| 5 | `main.py` | ✅ Done |
| 6 | `requirements.txt` + `README.md` | ✅ Done |

---

## 🚀 Quick Start (3 steps)
```

1. Copy all files into one folder
2. pip install requests
3. python main.py
