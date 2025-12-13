@echo off
echo ========================================
echo Emotion Music Recommender System Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found!
python --version
echo.

REM Check if virtual environment exists
if exist "emotion_env\" (
    echo [2/5] Virtual environment already exists.
) else (
    echo [2/5] Creating virtual environment...
    python -m venv emotion_env
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call emotion_env\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Initialize database
echo [5/5] Initializing database...
python database\init_database.py
if errorlevel 1 (
    echo [ERROR] Failed to initialize database!
    pause
    exit /b 1
)
echo Database initialized successfully!
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo   1. Run: emotion_env\Scripts\activate.bat
echo   2. Run: python app.py
echo   3. Open browser: http://localhost:5000
echo.
echo Default Admin Login:
echo   Username: admin
echo   Password: admin123
echo.
echo Press any key to start the application now...
pause >nul

REM Start the application
echo.
echo Starting application...
echo Press Ctrl+C to stop the server
echo.
python app.py
