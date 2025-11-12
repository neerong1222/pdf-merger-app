@echo off
REM Setup script for PDF Merger App (Windows)

echo.
echo 🔧 PDF Merger App - Setup Script
echo ==================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Create directories
echo 📁 Creating required directories...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
echo ✓ Directories created
echo.

REM Setup environment
if not exist ".env" (
    echo ⚙️  Creating .env from template...
    copy .env.example .env
    echo ✓ .env created - please update SECRET_KEY and other settings
) else (
    echo ✓ .env already exists
)
echo.

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your settings (especially SECRET_KEY)
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python app.py
echo 4. Visit: http://localhost:5000
echo.
pause
