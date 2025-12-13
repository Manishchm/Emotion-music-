#!/bin/bash

echo "========================================"
echo "Emotion Music Recommender System Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Python found!"
python3 --version
echo ""

# Check if virtual environment exists
if [ -d "emotion_env" ]; then
    echo "[2/5] Virtual environment already exists."
else
    echo "[2/5] Creating virtual environment..."
    python3 -m venv emotion_env
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment!"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source emotion_env/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment!"
    exit 1
fi
echo "Virtual environment activated!"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

# Initialize database
echo "[5/5] Initializing database..."
python database/init_database.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to initialize database!"
    exit 1
fi
echo "Database initialized successfully!"
echo ""

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Run: source emotion_env/bin/activate"
echo "  2. Run: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Default Admin Login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Enter to start the application now..."
read

# Start the application
echo ""
echo "Starting application..."
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
