@echo off
echo Starting Emotion Music Recommender System...
echo.

REM Check if virtual environment exists
if not exist "emotion_env\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to set up the application.
    pause
    exit /b 1
)

REM Activate virtual environment
call emotion_env\Scripts\activate.bat

REM Start the application
echo Application is starting on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
