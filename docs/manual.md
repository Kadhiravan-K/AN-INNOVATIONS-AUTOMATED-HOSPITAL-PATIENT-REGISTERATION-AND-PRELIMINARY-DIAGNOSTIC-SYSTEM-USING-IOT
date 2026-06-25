# Hospital Patient Registration System - User Manual

## 📋 Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Using the System](#using-the-system)
6. [Features](#features)
7. [Troubleshooting](#troubleshooting)
8. [FAQs](#faqs)

---

## Overview

The **Automated Hospital Patient Registration and Preliminary Diagnostic System** is an IoT-based kiosk that streamlines patient registration and initial health assessment in hospitals. The system captures vital signs, performs basic diagnostics, and automatically allocates patients to appropriate departments.

### Key Benefits

- ✅ Fast patient registration (< 5 minutes)
- ✅ Automated vital sign measurement
- ✅ Preliminary disease diagnosis
- ✅ Intelligent department allocation
- ✅ Emergency detection and prioritization

---

## Getting Started

### First Time Setup

1. **Power on the kiosk** - The system will initialize automatically
2. **Wait for startup** - The application loads all sensors (30-60 seconds)
3. **See the welcome screen** - Main menu appears when ready
4. **Follow on-screen instructions** - Touch screen interface guides you

---

## System Requirements

### Hardware

- **Processor**: Raspberry Pi 4B or equivalent
- **RAM**: 4GB minimum
- **Storage**: 32GB SD card recommended
- **Touch Screen**: 7-10 inch display recommended
- **Sensors**:
  - MLX90614 - Infrared temperature sensor
  - KY-039 - Pulse/heart rate sensor
  - BME280 - Environmental sensor (temp, humidity, pressure)

### Software

- **OS**: Raspberry Pi OS or Linux
- **Python**: 3.9 or higher
- **Database**: SQLite (included)

### Network

- Internet connection optional (for real Aadhaar API)
- Works in offline mock mode for testing

---

## Installation

### Step 1: Install Python

```bash
# Check if Python is installed
python --version

# If not, install Python 3.9+
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Install Dependencies

```bash
# Navigate to project folder
cd /path/to/hospital-registration-system

# Install required packages
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
# From project root directory
python -m app.main

# Or directly
python app/main.py
```

### Step 4: Hardware Connection (Raspberry Pi)

- Connect MLX90614 via I2C (pins 3, 5)
- Connect KY-039 to GPIO pin 17
- Connect BME280 via I2C
- Connect buzzer to GPIO pin 27

---

## Using the System

### Main Menu

The kiosk shows 5 main options:

1. **👤 New Patient Registration**
2. **🔐 Existing Patient Check-in**
3. ⚙️ **Settings** (Admin only)
4. ℹ️ **Help & Information**
5. 🚪 **Exit**

### New Patient Registration Flow

#### Step 1: Select Language

- Choose from available languages
- Instructions adapt to your selection

#### Step 2: Enter Aadhaar Number

- 12-digit Aadhaar ID required
- System validates format
- Displays registered name and DOB

#### Step 3: Aadhaar OTP Verification

- Enter OTP received on registered mobile
- 3 attempts allowed
- 10-minute timeout per session

#### Step 4: Confirm Demographics

- Review name, date of birth, gender
- Confirm or correct information
- Select mobile number for contact

#### Step 5: Select Symptoms

- Choose from symptom checklist
- Multiple symptoms can be selected
- Examples:
  - Fever, Cough, Difficulty breathing
  - Chest pain, Headache, Dizziness
  - Nausea, Vomiting, Abdominal pain

#### Step 6: Vital Sign Measurement

- **Temperature**: Place hand on infrared sensor
  - Wait 2-3 seconds for reading
  - Normal: 36.5°C - 37.5°C
- **Heart Rate**: Place finger on pulse sensor
  - Keep still for 5 seconds
  - Normal: 60-100 BPM
- **Environment**: Automatic reading
  - Displays ambient temperature, humidity, pressure

#### Step 7: Preliminary Diagnosis

- System analyzes symptoms + vital signs
- Determines:
  - Primary department
  - Doctor specialty needed
  - Emergency status (if applicable)

#### Step 8: Token & Receipt

- Receive **token number** for queue
- Print receipt with:
  - Registration ID
  - Assigned department
  - Doctor specialty
  - Estimated wait time
- Scan QR code to view digital receipt

---

## Features

### 🏥 Symptom Mapping

The system intelligently maps symptoms to departments:

| Symptoms                        | Department       | Doctor                 |
| ------------------------------- | ---------------- | ---------------------- |
| Fever, Cough, Chest pain        | Pulmonology      | Respiratory Specialist |
| Chest pain, Shortness of breath | Cardiology       | Cardiologist           |
| Headache, Nausea, Dizziness     | Neurology        | Neurologist            |
| Abdominal pain, Nausea          | Gastroenterology | Gastroenterologist     |
| Burns, Cuts, Injuries           | Emergency        | Trauma Surgeon         |

### 🚨 Emergency Detection

System automatically flags as emergency if:

- Temperature > 40°C (104°F)
- Heart rate > 120 BPM (resting)
- Heart rate < 50 BPM (resting)
- Multiple severe symptoms reported

### 📱 Digital Receipt

- QR code for quick reference
- Accessible on patient's phone
- Contains appointment details
- Can be used for check-in

### 🗄️ Database Security

- Patient data encrypted
- Compliant with healthcare privacy standards
- Local SQLite database
- Automatic backups

---

## Troubleshooting

### System Won't Start

**Problem**: Application doesn't launch

```bash
# Solution: Check Python is installed
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Run with verbose output
python -m app.main --debug
```

### Temperature Sensor Not Reading

**Problem**: "Temperature: Error" message

- Check MLX90614 connection (I2C pins)
- Ensure sensor is pointing correctly
- Wait for sensor warm-up (30 seconds)
- Restart system

### Heart Rate Sensor Unstable

**Problem**: Inconsistent or erratic readings

- Ensure finger is placed flat on sensor
- Keep still for full 5 seconds
- Clean sensor surface with soft cloth
- Try different finger

### Aadhaar Verification Fails

**Problem**: OTP not received or invalid

- Check mobile number on file
- Verify internet connection (if online mode)
- Request OTP again (new 6-digit code)
- Use mock mode for testing

### Database Locked Error

**Problem**: "Database is locked" message

- Close other instances of the app
- Wait 30 seconds and try again
- Check disk space (minimum 500MB)
- Restart system

### Touchscreen Not Responding

**Problem**: Screen taps not registered

- Calibrate touchscreen (Settings → Calibrate)
- Clean screen surface
- Check USB/power connections
- Restart application

---

## FAQs

### Q: Can the system work without internet?

**A:** Yes! The system has a **mock mode** that simulates all functions offline. In production, optional real Aadhaar verification requires internet.

### Q: How long does registration take?

**A:** Approximately 3-5 minutes per patient, depending on sensor readings and symptom selection.

### Q: Is my data secure?

**A:** Yes. Patient data is:

- Encrypted in local database
- Compliant with healthcare privacy laws
- Never transmitted without authorization
- Backed up regularly

### Q: What if I make a mistake during registration?

**A:** At any step before final submission:

- Tap **← Back** button to return to previous step
- Correct information and continue
- Start over option available in main menu

### Q: How accurate are the preliminary diagnostics?

**A:** The system provides **initial assessment only**:

- Not a medical diagnosis
- Should be reviewed by qualified doctor
- Helps route to appropriate department
- Speeds up triage process

### Q: Can I register without Aadhaar?

**A:** In mock/test mode: Yes, any 12-digit number works
In production: Aadhaar is required for legal compliance

### Q: What's the maximum patient capacity?

**A:** System can handle unlimited registrations. Daily capacity depends on:

- Hospital staff availability
- Doctor schedules
- Physical queue space
- Operating hours

### Q: How do I reset the system?

**A:**

```bash
# Stop current session
# Press Ctrl+C in terminal

# Clear database (DELETE - PERMANENT)
rm data/hospital_kiosk.db

# Restart application
python -m app.main
```

### Q: Where are patient records stored?

**A:** All records stored in:

```
data/hospital_kiosk.db
```

### Q: Can multiple kiosks work together?

**A:** Currently, each kiosk operates independently. For multi-kiosk deployment:

- Use network database (PostgreSQL/MySQL)
- Implement centralized server
- Contact development team for enterprise setup

---

## Support & Maintenance

### Regular Maintenance

- **Daily**: Clean touchscreen and sensors
- **Weekly**: Check database size and backups
- **Monthly**: Verify all sensors functioning
- **Quarterly**: Update software patches

### Sensor Calibration

- **Temperature**: Self-calibrating, no action needed
- **Heart Rate**: Check against manual pulse count
- **Environment**: Calibrate after temperature change

### Performance Tips

- Clear browser cache weekly
- Check disk space (keep > 1GB free)
- Restart system daily for optimal performance
- Monitor database size

### Emergency Contact

For technical support:

- **Email**: support@hospital-system.local
- **Phone**: Available on kiosk settings
- **On-site**: Technician available during business hours

---

## Version Information

- **System Version**: 1.0.0
- **Last Updated**: 2026-06-26
- **Supported Languages**: English, Hindi, Tamil (expandable)

---

**For more information, contact your Hospital IT Department**
