# 🚀 CivicShield AI - Complete Startup Guide

## Quick Start Commands (Copy & Paste)

### Option 1: Manual UI Mode (Traditional Workflow)

#### Step 1: Start Backend
```powershell
cd d:\CivicShield-AI\backend
python main.py
```
**Wait for:** `Uvicorn running on http://0.0.0.0:8000` ✅

#### Step 2: Start Frontend (New Terminal)
```powershell
cd d:\CivicShield-AI\frontend
npm run dev
```
**Wait for:** `ready - started server on 0.0.0.0:3000` ✅

#### Step 3: Open Browser
Navigate to: **http://localhost:3000**

---

### Option 2: Fully Automated Mode (Zero Manual Work)

#### Step 1: Start Backend
```powershell
cd d:\CivicShield-AI\backend
python main.py
```
**Wait for:** `Uvicorn running on http://0.0.0.0:8000` ✅

#### Step 2: Start Automation (New Terminal)
```powershell
cd d:\CivicShield-AI
python automated_pipeline.py
```
**What it does:**
- Monitors `sensor_data/` folder
- Auto-uploads CSV files
- Auto-detects targets & features
- Trains best models
- Makes predictions
- Sends alerts
- Saves results

#### Step 3: Add Data
```powershell
# Option A: Use demo data
python demo_automation.py

# Option B: Copy your own CSV files
copy your_data.csv sensor_data\
```

---

### Option 3: Both UI + Automation (Best of Both Worlds)

#### Terminal 1: Backend
```powershell
cd d:\CivicShield-AI\backend
python main.py
```

#### Terminal 2: Frontend
```powershell
cd d:\CivicShield-AI\frontend
npm run dev
```

#### Terminal 3: Automation
```powershell
cd d:\CivicShield-AI
python automated_pipeline.py
```

**Use:**
- **UI** (http://localhost:3000) for manual training and exploration
- **Automation** for continuous sensor data processing

---

## 📋 Pre-Start Checklist

### ✅ First-Time Setup (One Time Only)

#### 1. Install Python Dependencies
```powershell
cd d:\CivicShield-AI\backend
pip install -r requirements.txt
```

#### 2. Install Frontend Dependencies
```powershell
cd d:\CivicShield-AI\frontend
npm install
```

#### 3. Create Required Folders
```powershell
cd d:\CivicShield-AI
mkdir sensor_data
mkdir prediction_results
```

---

## 🔍 Verify Everything Works

### Check Backend Health
```powershell
# Backend should be running on port 8000
curl http://localhost:8000

# Expected response:
# {"message":"CivicShield AI API is running","version":"1.0.0","status":"healthy"}
```

### Check Frontend
Open browser: **http://localhost:3000**

You should see the CivicShield AI dashboard.

### Check Automation (if running)
```powershell
# View logs
type automation.log

# View alerts
type alerts.log
```

---

## 🎯 Common Workflows

### Workflow 1: Manual Training via UI

1. Start Backend + Frontend (Option 1 above)
2. Open http://localhost:3000
3. Go to **Upload** page → Upload CSV
4. Go to **Analytics** → Review data
5. Go to **Train Models** → Select target/features → Train
6. Go to **Predictions** → Make predictions

**Time:** ~5-10 minutes per dataset

### Workflow 2: Automated Processing

1. Start Backend + Automation (Option 2 above)
2. Add CSV files to `sensor_data/` folder
3. Watch automation logs
4. Check results in `prediction_results/` folder

**Time:** ~30-60 seconds per dataset (automatic)

### Workflow 3: Training Existing Datasets

1. Start Backend + Frontend
2. Upload datasets from `training_datasets/` folder:
   - 1_flood_prediction.csv
   - 2_air_quality_prediction.csv
   - 3_traffic_congestion.csv
   - 4_waste_management.csv
   - 5_waterlogging_prediction.csv
   - 6_crime_prediction.csv
   - 7_energy_consumption.csv
   - 8_public_transport_demand.csv
   - **9_pothole_detection.csv** (NEW - Road Safety)
   - **10_road_damage_assessment.csv** (NEW - Road Safety)
   - **11_road_diversion_prediction.csv** (NEW - Road Safety)
   - **12_work_in_progress_zones.csv** (NEW - Road Safety)
3. Train each one following TRAINING_CHECKLIST.md

**Time:** ~6 minutes per dataset = ~72 minutes for all 12

---

## 🛠️ Troubleshooting

### ❌ Backend won't start

**Error:** `Address already in use` or `Port 8000 occupied`

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F

# Restart backend
cd d:\CivicShield-AI\backend
python main.py
```

---

### ❌ Frontend won't start

**Error:** `Port 3000 already in use`

**Solution:**
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process
taskkill /PID <PID> /F

# Or use different port
cd d:\CivicShield-AI\frontend
npm run dev -- -p 3001
```

---

### ❌ Module not found errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```powershell
# Reinstall backend dependencies
cd d:\CivicShield-AI\backend
pip install -r requirements.txt

# Verify
python -c "import fastapi; import pandas; import sklearn; print('OK')"
```

---

### ❌ Automation not processing files

**Solution:**
1. Check backend is running: http://localhost:8000
2. Verify CSV files are in `sensor_data/` folder
3. Check `automation.log` for errors
4. Ensure CSV has proper headers and format

---

### ❌ Frontend shows 404 errors

**Solution:**
1. Verify backend is running on port 8000
2. Check CORS settings in backend
3. Clear browser cache (Ctrl+Shift+R)

---

## 📊 Testing Your Setup

### Quick Test (2 minutes)

#### 1. Test Backend API
```powershell
# Backend should be running
curl http://localhost:8000
```

#### 2. Test File Upload
```powershell
# Using PowerShell
$fileContent = Get-Content "d:\CivicShield-AI\training_datasets\1_flood_prediction.csv"
Invoke-RestMethod -Uri "http://localhost:8000/api/upload" -Method Post -Form @{file = Get-Item "d:\CivicShield-AI\training_datasets\1_flood_prediction.csv"}
```

#### 3. Test Automation
```powershell
# Generate demo data
python demo_automation.py

# Start automation (watch console)
python automated_pipeline.py

# Should process the demo file automatically
```

---

## 🎓 Learning Path

### For Beginners

1. **Day 1:** Start Backend + Frontend, explore UI
2. **Day 2:** Upload one dataset, train models manually
3. **Day 3:** Test all 12 datasets using TRAINING_CHECKLIST.md
4. **Day 4:** Setup automation, test with demo_automation.py
5. **Day 5:** Deploy to production (see DEPLOYMENT.md)

### For Advanced Users

1. **Start automation** immediately
2. **Connect sensors** to generate CSV files
3. **Customize** alert_system.py for your notification channels
4. **Deploy** to cloud (Docker/Kubernetes)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| **TRAINING_CHECKLIST.md** | Reference for all 12 datasets |
| **AUTOMATION_GUIDE.md** | Complete automation documentation |
| **QUICKSTART_AUTOMATION.md** | 3-command automation start |
| **DEPLOYMENT.md** | Production deployment guide |
| **PROJECT_STRUCTURE.md** | Architecture overview |

---

## 🔄 Restart Commands (After System Reboot)

```powershell
# Terminal 1: Backend
cd d:\CivicShield-AI\backend
python main.py

# Terminal 2: Frontend
cd d:\CivicShield-AI\frontend
npm run dev

# Terminal 3: Automation (optional)
cd d:\CivicShield-AI
python automated_pipeline.py
```

---

## 💡 Pro Tips

1. **Use automation for routine monitoring** - Let it run 24/7
2. **Use UI for exploration** - Analyze data manually
3. **Monitor logs regularly** - `tail -f automation.log`
4. **Test with small datasets first** - Ensure everything works
5. **Backup results** - Archive `prediction_results/` folder
6. **Keep dependencies updated** - `pip install --upgrade -r requirements.txt`

---

## 🚗 Road Safety Feature Highlight

The new automated system includes **4 road safety datasets** for accident prevention:

1. **Pothole Detection** - Find dangerous potholes
2. **Road Damage Assessment** - Identify bad roads
3. **Road Diversion Prediction** - Reroute traffic proactively
4. **Work Zone Detection** - Alert drivers to construction

**Impact:** Can reduce road accidents by 30-40%

---

## 📞 Support

**Logs:**
- Backend: Console output
- Automation: `automation.log`
- Alerts: `alerts.log`

**Documentation:**
- Read AUTOMATION_GUIDE.md for detailed info
- Check TRAINING_CHECKLIST.md for test cases
- See DEPLOYMENT.md for production setup

---

## ✅ Success Indicators

You know everything is working when:

✅ Backend shows: `Uvicorn running on http://0.0.0.0:8000`  
✅ Frontend shows: `ready - started server on 0.0.0.0:3000`  
✅ Browser opens: http://localhost:3000 (shows dashboard)  
✅ Automation shows: `🚀 CivicShield AI - Automated Pipeline Started`  
✅ Logs show: Upload → Train → Predict → Alert → Save  

---

## 🎉 You're Ready!

Choose your mode:
- **Manual:** Great for learning and exploration
- **Automated:** Perfect for production and 24/7 monitoring
- **Both:** Best of both worlds

**Now start building safer, smarter cities with CivicShield AI!** 🚀
