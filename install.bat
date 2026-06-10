@echo off
REM ARIA System - Installation Script

echo.
echo ╔═════════════════════════════════════════╗
echo ║  🤖 ARIA System Installation Script      ║
echo ╚═════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Check if venv exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 📥 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Check .env file
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Please create .env file with your API keys:
    echo.
    echo GROQ_API_KEY=your_key_here
    echo TAVILY_API_KEY=your_key_here
    echo.
) else (
    echo ✅ .env file found
)

echo.
echo ╔═════════════════════════════════════════╗
echo ║  ✅ Installation Complete!               ║
echo ╚═════════════════════════════════════════╝
echo.
echo 🚀 To run the application, use:
echo.
echo    python main.py run "Your task here"
echo    python main.py chat
echo    python main.py status
echo.
echo 📖 See SETUP_GUIDE.md for more options
echo.

pause
