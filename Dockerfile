# ─────────────────────────────────────────────────────────────────
# Dockerfile — For simplified deployment of the Hospital Kiosk
# ─────────────────────────────────────────────────────────────────

# Use official Python lightweight image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for Tkinter and GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the Admin Dashboard port
EXPOSE 8080

# Default command to run the main application
# Note: For GUI to work in Docker, you need to map the X11 display
CMD ["python", "main.py"]
