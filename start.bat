@echo off
echo ================================
echo CivicShield AI - Quick Start
echo ================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Creating required directories...
if not exist "exports" mkdir exports

echo Starting backend server...
start "Backend Server" cmd /k "venv\Scripts\activate && python main.py"

echo.
echo [2/4] Backend server started on http://localhost:8000
echo.
timeout /t 5

echo [3/4] Setting up Frontend...
cd ..\frontend

echo Installing dependencies...
call npm install

echo Creating environment file...
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

echo [4/4] Starting frontend...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
