@echo off
REM ============================================================================
REM Nirikshan — Environment Setup Script (Windows Batch)
REM ============================================================================

setlocal enabledelayedexpansion

echo ========================================================
echo Nirikshan - Packaged Commodity Compliance Auditor
echo Setting up local development environment...
echo ========================================================

REM Navigate to project root
cd /d "%~dp0\.."

REM Step 1: Initialize project directories and packages
echo.
echo [Step 1] Initializing directory structure...
python scripts\init_project.py

REM Step 2: Create Python Virtual Environment
echo.
echo [Step 2] Creating virtual environment (venv)...
if not exist "venv" (
    python -m venv venv
    echo   Virtual environment created at .\venv
) else (
    echo   Virtual environment already exists at .\venv
)

REM Step 3: Activate Virtual Environment
echo.
echo [Step 3] Activating virtual environment...
call venv\Scripts\activate.bat
echo   Virtual environment activated.

REM Step 4: Upgrade pip, setuptools, wheel
echo.
echo [Step 4] Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

REM Step 5: Install backend dependencies
echo.
echo [Step 5] Installing Python dependencies from backend\requirements.txt...
if exist "backend\requirements.txt" (
    pip install -r backend\requirements.txt
    echo   Dependencies installed successfully.
) else (
    echo   backend\requirements.txt not found!
    exit /b 1
)

echo.
echo ========================================================
echo Setup complete! Nirikshan is ready for use.
echo ========================================================
echo.
echo To run the Nirikshan server:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Start the FastAPI application server:
echo      cd backend
echo      uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo   3. Open your browser:
echo      - Scanner UI:    http://localhost:8000
echo      - Dashboard:     http://localhost:8000/dashboard
echo      - API Docs:      http://localhost:8000/docs
echo ========================================================

endlocal
