# Project Structure

```
hospital-registration-system/
├── app/                          # Main application code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Entry point - Run this to start
│   ├── config.py                # Configuration and settings
│   ├── database.py              # Database operations (SQLite)
│   ├── auth.py                  # Authentication logic (Aadhaar OTP)
│   └── sensors.py               # IoT sensor logic (MLX90614, KY-039, BME280)
│
├── tests/                       # Unit tests and integration tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_database.py
│   └── test_sensors.py
│
├── data/                        # Data files and databases
│   └── hospital_kiosk.db        # SQLite database (generated at runtime)
│
├── docs/                        # Documentation
│   └── README.md                # Project documentation
│
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── .gitignore                   # Git ignore rules
├── LICENSE                      # License file
└── README.md                    # Main project readme

```

## File Organization Guide

### app/ Directory

- **main.py**: Main application entry point
- **config.py**: All configuration settings centralized
- **database.py**: Database operations and schema
- **auth.py**: Aadhaar authentication logic
- **sensors.py**: IoT sensor implementations

### tests/ Directory

- Unit tests for each module
- Integration tests
- Mock sensor tests

### data/ Directory

- SQLite database files (auto-generated)
- Keep generated data files here

### docs/ Directory

- Project documentation
- API documentation
- Setup guides

## Running the Application

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to project root and run:
   ```bash
   python -m app.main
   ```

Or from within the project directory:

```bash
python app/main.py
```

## Best Practices Applied

✅ Organized package structure with proper `app/` module  
✅ Separated tests in dedicated directory  
✅ Configuration centralized  
✅ `.gitignore` excludes unnecessary files  
✅ Clear documentation structure  
✅ Setup.py for proper package management
