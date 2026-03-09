# CivicShield AI - Setup Guide

Complete step-by-step guide to set up and run CivicShield AI locally.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Docker Setup](#docker-setup)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

#### Windows
- **Python 3.9+**: Download from [python.org](https://www.python.org/downloads/)
- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)
- **Git**: Download from [git-scm.com](https://git-scm.com/)

#### Mac/Linux
```bash
# Install Python
brew install python@3.9  # Mac
sudo apt install python3.9  # Linux

# Install Node.js
brew install node  # Mac
sudo apt install nodejs npm  # Linux
```

### Verify Installation
```bash
python --version  # Should show 3.9 or higher
node --version    # Should show 18 or higher
npm --version     # Should show 9 or higher
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pandas - Data manipulation
- NumPy - Numerical computing
- Scikit-learn - Machine learning
- Joblib - Model persistence

### Step 4: Create Required Directories
```bash
# Windows
mkdir exports
mkdir models

# Mac/Linux
mkdir -p exports models
```

### Step 5: Run the Backend Server
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Verify Backend is Running
Open browser and navigate to:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

You should see the API documentation.

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory
Open a **NEW** terminal window (keep backend running) and run:
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This will install all required packages including:
- React & Next.js
- Tailwind CSS
- Chart.js & Plotly
- Leaflet for maps
- Axios for API calls
- Framer Motion for animations

### Step 3: Create Environment File
Create a file named `.env.local` in the frontend directory:

#### Windows
```bash
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
```

#### Mac/Linux
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

Or manually create `.env.local` with this content:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Run Development Server
```bash
npm run dev
```

### Step 5: Verify Frontend is Running
Open browser and navigate to:
- Frontend: http://localhost:3000

You should see the CivicShield AI landing page.

---

## Docker Setup (Alternative)

If you prefer using Docker:

### Step 1: Install Docker
- Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

### Step 2: Build and Run
```bash
# From project root directory
docker-compose up --build
```

This will:
1. Build backend and frontend images
2. Start both services
3. Backend: http://localhost:8000
4. Frontend: http://localhost:3000

### Step 3: Stop Services
```bash
docker-compose down
```

---

## Using the Application

### 1. Upload a Dataset
1. Navigate to http://localhost:3000
2. Click "Get Started" or "Upload Data"
3. Drag and drop a CSV file or click to browse
4. View dataset preview and statistics

### 2. Analyze Data
1. Go to "Analytics" page from sidebar
2. View comprehensive statistics
3. See missing values chart
4. Check column type distribution

### 3. Visualize Data
1. Navigate to "Visualizations"
2. Explore correlation heatmap
3. Select columns for distribution analysis
4. View feature relationships

### 4. Train ML Models
1. Go to "Train Models"
2. Select target column (what to predict)
3. Choose feature columns (inputs)
4. Select models to train
5. Click "Train Models"
6. View performance metrics
7. Check feature importance

### 5. Make Predictions
1. Navigate to "Predictions"
2. Select trained model
3. Enter input values
4. Click "Make Prediction"
5. View results

### 6. Map Visualization
1. Go to "Map View"
2. View geographical data (requires lat/lon columns)
3. Click markers for details

---

## Troubleshooting

### Backend Issues

#### Port 8000 Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

#### Module Not Found Error
```bash
# Activate virtual environment first
pip install -r requirements.txt
```

#### Permission Denied (Linux/Mac)
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Frontend Issues

#### Port 3000 Already in Use
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

Or change port:
```bash
npm run dev -- -p 3001
```

#### Module Not Found
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### Connection Issues

#### Frontend Can't Connect to Backend
1. Verify backend is running at http://localhost:8000
2. Check `.env.local` has correct API URL
3. Restart frontend: `Ctrl+C` then `npm run dev`

#### CORS Errors
Backend is configured to allow all origins in development. If issues persist:
1. Check backend logs
2. Verify FastAPI CORS middleware configuration

### Data Upload Issues

#### File Upload Fails
1. Verify file is CSV or Excel format
2. Check file encoding (UTF-8 recommended)
3. Ensure file size is reasonable (< 100MB)
4. Check for special characters in column names

#### Missing Value Errors
1. The system handles missing values automatically
2. Use "Data Cleaning" options in Analytics
3. Check data types are correct

---

## Development Tips

### Hot Reload
Both backend and frontend support hot reload:
- Backend: Auto-reloads on file changes
- Frontend: Auto-refreshes browser on changes

### Debug Mode
Enable debug logging:

Backend:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Frontend:
Check browser console (F12) for errors

### API Testing
Use the interactive API docs:
- http://localhost:8000/docs

### Sample Dataset
Create a sample CSV for testing:
```csv
x1,x2,x3,y
1,2,3,10
4,5,6,15
7,8,9,20
10,11,12,25
```

---

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
npm start
```

### Backend Production Server
```bash
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables
Set in production:
```env
# Frontend
NEXT_PUBLIC_API_URL=https://your-api-domain.com

# Backend (if needed)
ENVIRONMENT=production
```

---

## Getting Help

### Check Logs
- Backend: Terminal where you ran `python main.py`
- Frontend: Terminal where you ran `npm run dev`
- Browser: Console (F12)

### Common Issues
1. **"Connection Refused"**: Backend not running
2. **"404 Not Found"**: Wrong API URL in `.env.local`
3. **"Cannot read property"**: Frontend waiting for data
4. **"Module not found"**: Missing dependencies

### Still Need Help?
1. Check GitHub issues
2. Review API documentation at /docs
3. Verify all dependencies are installed
4. Ensure both servers are running

---

**Happy coding! 🚀**
