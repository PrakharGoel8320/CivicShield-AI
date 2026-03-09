# CivicShield AI - Urban Solutions Platform 🌆

![CivicShield AI](https://img.shields.io/badge/CivicShield-AI%20v2.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)
![Automation](https://img.shields.io/badge/Automation-Enabled-brightgreen)

A professional full-stack AI platform for urban data analysis, machine learning, and visualization with **fully automated prediction pipelines** and **intelligent detection**. Built for the Circuit Minds Hackathon.

## 🚀 What's New in v2.0

- **🤖 Fully Automated Pipeline**: Sensor data → CSV → Auto-upload → Auto-train → Predictions → Alerts (zero manual intervention!)
- **🧠 Intelligent Detection**: Automatically detects target columns and selects optimal features using mutual information
- **🚨 Multi-Channel Alerts**: Real-time notifications via console, email, and webhooks for high-risk predictions
- **🛣️ Road Safety Models**: 4 new datasets for pothole detection, road damage assessment, diversions, and work zones
- **📊 12 Pre-built Datasets**: Flood, AQI, traffic, waste management, waterlogging, crime, energy, and more!

## 🌟 Features

### 🤖 Automation (NEW!)
- **🔄 Zero-Touch Pipeline** - Sensor data automatically processed, trained, and predicted
- **🧠 Intelligent Detection** - Auto-detects target columns and selects optimal features
- **🚨 Smart Alerts** - Real-time notifications when predictions exceed risk thresholds
- **📁 File Monitoring** - Watches `sensor_data/` folder and processes new CSV files automatically
- **📊 Auto-Training** - Models train themselves when new data arrives
- **💾 Result Storage** - Predictions saved with original data in `prediction_results/`

### Data Management
- 📁 **CSV/Excel Upload** - Import datasets easily (manual or automated)
- 🧹 **Data Cleaning** - Handle missing values, duplicates, and outliers
- 🔧 **Feature Engineering** - Create new features automatically
- 📊 **Data Preview** - View and analyze your data
- 🔍 **Feature Selection** - Intelligent mutual information-based selection

### Machine Learning
- 🤖 **Multiple Models** - Linear Regression, Random Forest, Decision Tree, Gradient Boosting, SVM, Logistic Regression
- 📈 **Model Training** - Train and compare multiple models (manual or auto-detect)
- 🎯 **Predictions** - Make single and batch predictions with confidence scores
- 📉 **Feature Importance** - Understand model decisions with feature rankings
- 🏆 **Auto Model Selection** - System recommends best models based on target type

### Visualizations
- 📊 **Interactive Charts** - Bar, Line, Scatter plots
- 🔥 **Correlation Heatmap** - Understand feature relationships
- 📈 **Distribution Analysis** - Visualize data distributions
- 🗺️ **Map Visualization** - Geographical data with Leaflet

### User Experience
- 🎨 **Modern UI** - Professional SaaS-style dashboard
- 🌙 **Dark Mode** - Easy on the eyes
- 📱 **Responsive** - Works on all devices
- ⚡ **Fast & Smooth** - Optimized performance
- 🔔 **Alert Notifications** - Real-time alerts for high-risk predictions

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI** - Modern API framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Joblib** - Model persistence

### Frontend
- **React 18** - UI library
- **Next.js 14** - React framework
- **Tailwind CSS** - Styling
- **Chart.js** - Charts
- **Plotly** - Advanced visualizations
- **Leaflet** - Maps
- **Framer Motion** - Animations
- **Axios** - HTTP client

### Automation (NEW!)
- **Watchdog** - File system monitoring
- **Requests** - HTTP client for API calls
- **SMTP/Webhook** - Alert notifications
- **Mutual Information** - Feature importance scoring

## 📦 Pre-built Datasets (12 Total)

### Urban Monitoring (8 Datasets)
1. **Flood Prediction** - Rainfall, river levels, temperature → flood risk (1-5)
2. **Air Quality Index** - Temperature, humidity, wind, traffic → AQI value
3. **Traffic Congestion** - Speed, incidents, weather → congestion level (1-5)
4. **Waste Generation** - Households, bins, events → waste per capita
5. **Waterlogging Risk** - Drainage, rainfall, pumps → waterlogging level (1-5)
6. **Crime Prediction** - Unemployment, income, education → crime risk (1-5)
7. **Energy Consumption** - Building size, AC usage, occupancy → kWh consumption
8. **Public Transport** - Ridership, weather, routes → passenger count

### Road Safety (4 Datasets - NEW!)
9. **Pothole Detection** - Vibration, surface roughness, cracks → pothole severity (1-5)
10. **Road Damage Assessment** - Pavement condition, rutting, cracking → damage level (1-5)
11. **Road Diversion** - Traffic density, accidents, road work → diversion needed (0/1)
12. **Work Zone Detection** - Construction vehicles, workers, barriers → work in progress (0/1)

> **Ready to Use**: All 12 datasets are in `training_datasets/` with 50-60 samples each. See [TRAINING_CHECKLIST.md](TRAINING_CHECKLIST.md) for training instructions.

## 📁 Project Structure

```
CivicShield-AI/
├── backend/
│   ├── main.py                    # FastAPI server with auto-train endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   └── ml_models.py           # ML model training (6 models)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_preprocessing.py  # Data cleaning
│   │   ├── feature_engineering.py # Feature creation
│   │   ├── intelligent_detector.py # Auto-detect targets/features (NEW!)
│   │   └── alert_system.py        # Multi-channel alerts (NEW!)
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── pages/
│   │   ├── index.tsx              # Landing page
│   │   ├── dashboard.tsx          # Main dashboard
│   │   ├── upload.tsx             # Data upload
│   │   ├── analytics.tsx          # Data analytics
│   │   ├── visualizations.tsx     # Charts & graphs
│   │   ├── train.tsx              # Model training
│   │   ├── predictions.tsx        # Predictions
│   │   └── map.tsx                # Map view
│   ├── components/
│   │   └── Layout.tsx             # App layout
│   ├── styles/
│   │   └── globals.css            # Global styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── README.md
├── training_datasets/             # 12 pre-built datasets (NEW!)
│   ├── 1_flood_prediction.csv
│   ├── 2_air_quality_index.csv
│   ├── 3_traffic_congestion.csv
│   ├── 4_waste_generation.csv
│   ├── 5_waterlogging_risk.csv
│   ├── 6_crime_prediction.csv
│   ├── 7_energy_consumption.csv
│   ├── 8_public_transport_ridership.csv
│   ├── 9_pothole_detection.csv           # Road safety (NEW!)
│   ├── 10_road_damage_assessment.csv     # Road safety (NEW!)
│   ├── 11_road_diversion_prediction.csv  # Road safety (NEW!)
│   └── 12_work_in_progress_zones.csv     # Road safety (NEW!)
├── sensor_data/                   # Monitored by automation pipeline (NEW!)
├── prediction_results/            # Auto-saved predictions (NEW!)
├── automated_pipeline.py          # Main automation service (NEW!)
├── demo_automation.py             # Quick test script (NEW!)
├── AUTOMATION_GUIDE.md            # 500+ line automation docs (NEW!)
├── QUICKSTART_AUTOMATION.md       # 3-command quick start (NEW!)
├── TRAINING_CHECKLIST.md          # Training guide for 12 datasets (UPDATED!)
├── STARTUP.md                     # Complete startup commands (NEW!)
├── PROJECT_STRUCTURE.md           # Detailed structure docs
├── DEPLOYMENT.md                  # Production deployment guide
├── GITHUB_CHECKLIST.md            # GitHub upload checklist
├── CHANGELOG.md                   # Version 2.0 changelog (NEW!)
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

> **💡 Choose Your Mode**: Manual UI (traditional training) or Fully Automated (zero-touch pipeline)

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

### ⚡ Option 1: Fully Automated Mode (Recommended!)

**Start the automation pipeline in 3 commands:**

```powershell
# 1. Start backend
cd backend
python main.py

# 2. Start automation (new terminal)
cd ..
python automated_pipeline.py

# 3. Add sensor data (new terminal)
python demo_automation.py
# OR copy your own CSV files to sensor_data/
```

**What happens automatically:**
1. 📁 System monitors `sensor_data/` folder every 30 seconds
2. 📤 New CSV files uploaded to backend
3. 🤖 Target column and features auto-detected using mutual information
4. 🎓 Best model trained automatically
5. 🔮 Predictions made for all rows
6. 🚨 Alerts sent if predictions exceed risk thresholds
7. 💾 Results saved to `prediction_results/` with predictions appended

> **📖 Full Guide**: See [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) for complete documentation

### 🖥️ Option 2: Manual UI Mode (Traditional)

**Start the web interface:**

```powershell
# 1. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py

# 2. Frontend Setup (new terminal)
cd frontend
npm install
npm run dev
```

**Then open**: `http://localhost:3000`

> **📖 Manual Training Guide**: See [TRAINING_CHECKLIST.md](TRAINING_CHECKLIST.md) for 12 pre-built datasets

### 🔀 Option 3: Both Modes (Hybrid)

Run backend + frontend + automation simultaneously:

```powershell
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Automation
cd ..
python automated_pipeline.py
```

> **📖 Complete Startup Guide**: See [STARTUP.md](STARTUP.md) for all commands, troubleshooting, and testing

The backend will be available at `http://localhost:8000` and frontend at `http://localhost:3000`

## 🎨 Screenshots

### Landing Page
Modern, professional landing page with hero section and features overview.

### Dashboard
Beautiful SaaS-style dashboard with statistics, quick actions, and system status.

### Data Upload
Intuitive drag-and-drop interface for dataset uploads with instant preview.

### Analytics
Comprehensive data analysis with charts, statistics, and missing value analysis.

### Model Training
Easy-to-use interface for training multiple ML models with performance metrics.

### Predictions
Simple prediction interface with real-time results and probability visualization.

### Map View
Interactive geographical visualization with Leaflet maps.

### Automation Logs (NEW!)
Real-time monitoring of automated pipeline with alerts and processing status.

## 📊 Performance Stats

- **🤖 Automation**: 100% hands-free from sensor data to predictions
- **📦 Datasets**: 12 pre-built urban & road safety datasets
- **🎯 Accuracy**: 85-99% on test datasets (varies by model)
- **⚡ Speed**: < 2 minutes per dataset (auto-train + predict)
- **📈 Scalability**: Handles 50-10,000 rows efficiently
- **🔔 Alerts**: Real-time notifications for high-risk predictions

## 🎯 API Endpoints

### 🤖 Automated Workflow (Zero-Touch)

**Perfect for**: IoT sensors, continuous monitoring, production deployments

1. **Start the automation pipeline**:
   ```powershell
   python automated_pipeline.py
   ```

2. **Add sensor data**:
   ```powershell
   # Option A: Demo data
   python demo_automation.py
   
   # Option B: Your own data
   copy your_sensor_data.csv sensor_data\
   ```

3. **Watch the magic happen**:
   - System automatically uploads, trains, predicts, and alerts
   - Monitor logs: `type automation.log` or `type alerts.log`
   - Results saved in `prediction_results/` with predictions appended

**No manual intervention needed!** The system:
- ✅ Detects target column (flood_risk_level, pothole_severity, etc.)
- ✅ Selects best features using mutual information
- ✅ Recommends optimal models (RF, GB, Linear, etc.)
- ✅ Trains and evaluates automatically
- ✅ Makes predictions for all rows
- ✅ Sends alerts if thresholds exceeded
- ✅ Saves results with original data

### 🖥️ Manual UI Workflow (Interactive)

**Perfect for**: Data exploration, model experimentation, learning

#### 1. Upload Dataset
- Navigate to "Upload Data" page
- Drag and drop your CSV/Excel file or click to browse
- View dataset preview and statistics

#### 2. Analyze Data
- Go to "Analytics" page
- View data statistics, missing values, and distributions
- See data types and column information

#### 3. Visualize Data
- Visit "Visualizations" page
- Explore correlation heatmap
- View distribution charts for each column
- Analyze feature relationships

#### 4. Train Models
- Navigate to "Train Models" page
- Select target column (what to predict)
- Choose feature columns (input variables) **OR** enable auto-detection
- Select models to train (or let system recommend)
- Click "Train Models"
- Compare model performance (R², Accuracy, MAE, RMSE)

#### 5. Make Predictions
- Go to "Predictions" page
- Select trained model
- Enter input values
- Click "Make Prediction"
- View prediction results with confidence

#### 6. Map Visualization
- Visit "Map View" page
- View geographical data on interactive map
- Click markers for detailed information

### 📊 Training Pre-built Datasets

Train all 12 urban monitoring datasets manually:

```powershell
# Follow the checklist
# See TRAINING_CHECKLIST.md for:
# - Exact columns to use
# - Expected accuracy scores
# - Test prediction values
# - Time estimate: ~72 minutes for all 12 datasets
```

## 🎯 API Endpoints

### Data Management
- `POST /api/upload` - Upload dataset
- `GET /api/data/preview` - Get data preview
- `GET /api/data/statistics` - Get statistics
- `POST /api/data/clean` - Clean dataset
- `POST /api/data/feature-engineering` - Feature engineering

### Machine Learning
- `POST /api/ml/train` - Train models (manual mode)
- `POST /api/ml/auto-train` - Train with auto-detection (NEW!)
- `POST /api/ml/predict` - Make prediction
- `POST /api/ml/batch-predict` - Batch predictions
- `GET /api/models/available` - Get available models

### Visualization
- `GET /api/visualization/correlation` - Correlation matrix
- `GET /api/visualization/distribution/{column}` - Distribution data
- `GET /api/map/data` - Map data

### Export
- `POST /api/export` - Export data

> **📚 Interactive API Docs**: Visit `http://localhost:8000/docs` for Swagger UI

## 🎨 Screenshots

### Landing Page
Modern, professional landing page with hero section and features overview.

### Dashboard
Beautiful SaaS-style dashboard with statistics, quick actions, and system status.

### Data Upload
Intuitive drag-and-drop interface for dataset uploads with instant preview.

### Analytics
Comprehensive data analysis with charts, statistics, and missing value analysis.

### Model Training
Easy-to-use interface for training multiple ML models with performance metrics.

### Predictions
Simple prediction interface with real-time results and probability visualization.

### Map View
Interactive geographical visualization with Leaflet maps.

## 🤝 Contributing

This project was built for the Circuit Minds Hackathon. Feel free to fork and customize for your needs.

## 📄 License

This project is open source and available under the MIT License.

## 🏆 Hackathon Project

Built for Circuit Minds - Urban Solutions Challenge 2026

### Team
- Full-stack AI Platform
- Data Science & ML Pipeline
- Modern UI/UX Design

## 🔗 Links

- Backend API Documentation: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

## 💡 Tips

### For Automated Mode:
1. **File Format**: CSV files in `sensor_data/` should have headers and clean data
2. **Alert Thresholds**: Customize in `automated_pipeline.py` (default: flood_risk >4, pothole_severity >4, AQI >150)
3. **Check Intervals**: Pipeline checks for new files every 30 seconds (configurable)
4. **Email Alerts**: Configure SMTP settings in `backend/utils/alert_system.py` for email notifications
5. **Monitoring**: Watch `automation.log` for pipeline activity, `alerts.log` for high-risk predictions

### For Manual Mode:
1. **Data Format**: Ensure your CSV has proper headers and clean data
2. **Missing Values**: The system handles missing values automatically
3. **Feature Selection**: Use auto-detection or choose relevant features manually
4. **Model Selection**: Try multiple models to find the best fit (system recommends based on target type)
5. **Visualization**: Use correlation heatmap to understand feature relationships

### General Tips:
- **First Time?** Start with demo_automation.py to see the system in action (2-minute test)
- **Production Use**: Run both frontend (exploration) + automation (monitoring) for best experience
- **Dataset Size**: System handles 50-10,000 rows efficiently; larger datasets may need optimization
- **Model Performance**: R² >0.80 or Accuracy >85% indicates good model performance

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 occupied**: Run `netstat -ano | findstr :8000` and `taskkill /PID <PID> /F`
- **Module not found**: Activate venv and run `pip install -r requirements.txt`
- **Python version**: Ensure Python 3.9+ is installed (`python --version`)

### Frontend Issues
- **Port 3000 occupied**: Use `npm run dev -- -p 3001` for different port
- **Build fails**: Clear `.next` folder: `rmdir /s .next` (Windows) or `rm -rf .next` (Linux/Mac)
- **Node version**: Ensure Node.js 18+ is installed (`node --version`)

### Automation Issues (NEW!)
- **Files not processing**: 
  1. Check backend is running (`curl http://localhost:8000`)
  2. Verify CSV files are in `sensor_data/` folder
  3. Check `automation.log` for errors
  4. Ensure CSV has proper headers and at least 10 rows
  
- **No alerts appearing**:
  1. Check predictions exceed thresholds (default: flood_risk >4, AQI >150)
  2. View `alerts.log` and `alerts.jsonl` for alert history
  3. Verify alert thresholds in `automated_pipeline.py`
  
- **Auto-detection failing**:
  1. Ensure dataset has >10 numeric columns for best results
  2. Check column names contain keywords (risk, level, severity, etc.)
  3. Review `automation.log` for detection results

### Data Upload Issues
- **File format error**: Verify CSV/Excel file format and encoding (UTF-8 recommended)
- **File too large**: Keep files under 100MB for optimal performance
- **Missing columns**: Ensure column names don't have special characters

### Model Training Issues
- **Low accuracy**: Try different feature combinations or enable auto-detection
- **Training timeout**: Reduce dataset size or use fewer models
- **Memory errors**: Close other applications or increase system RAM

> **📖 Full Troubleshooting Guide**: See [STARTUP.md](STARTUP.md) for comprehensive solutions

## 📞 Support

For issues or questions, please create an issue in the repository.

## 📚 Documentation

- **[STARTUP.md](STARTUP.md)** - Complete startup guide with all commands and modes
- **[AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)** - 500+ line comprehensive automation documentation
- **[QUICKSTART_AUTOMATION.md](QUICKSTART_AUTOMATION.md)** - 3-command quick start for automation
- **[TRAINING_CHECKLIST.md](TRAINING_CHECKLIST.md)** - Manual training guide for 12 pre-built datasets
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Detailed project architecture
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide (Docker, PaaS, VPS)
- **[GITHUB_CHECKLIST.md](GITHUB_CHECKLIST.md)** - GitHub upload preparation checklist
- **[CHANGELOG.md](CHANGELOG.md)** - Version 2.0 changelog and migration guide

## 🚀 Production Deployment

This project is production-ready! Choose your deployment method:

1. **Docker**: `docker-compose up -d` (simplest)
2. **Platform as a Service**: Heroku (backend) + Vercel (frontend)
3. **VPS**: Ubuntu/CentOS with nginx reverse proxy

> **📖 Full Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions

## 🤝 Contributing

This project was built for the Circuit Minds Hackathon. Feel free to fork and customize for your needs.

### Key Features to Extend:
- Add more ML models (XGBoost, LightGBM, Neural Networks)
- Integrate real IoT sensors (MQTT, HTTP webhooks)
- Add database support (PostgreSQL, MongoDB)
- Create mobile apps (React Native, Flutter)
- Implement user authentication (JWT, OAuth)

---

**Version 2.0** - Now with Full Automation! 🚀
