@echo off
echo ========================================================
echo   Starting Nirikshan Packaged Commodity Auditor Engine
echo ========================================================

IF NOT EXIST "venv" (
    echo Creating Python Virtual Environment...
    python -m venv venv
)

echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Launching Nirikshan Server...
set PYTHONPATH=backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
