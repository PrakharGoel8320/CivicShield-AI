#!/bin/bash

echo "================================"
echo "CivicShield AI - Quick Start"
echo "================================"
echo ""

echo "[1/4] Setting up Backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating required directories..."
mkdir -p exports

echo "Starting backend server..."
python main.py &
BACKEND_PID=$!

echo ""
echo "[2/4] Backend server started on http://localhost:8000"
echo ""
sleep 5

echo "[3/4] Setting up Frontend..."
cd ../frontend

echo "Installing dependencies..."
npm install

echo "Creating environment file..."
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

echo "[4/4] Starting frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user interrupt
wait
