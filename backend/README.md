# CivicShield AI - Backend

FastAPI backend for CivicShield AI platform.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Data Management
- `POST /api/upload` - Upload CSV dataset
- `GET /api/data/preview` - Get data preview
- `GET /api/data/statistics` - Get dataset statistics
- `POST /api/data/clean` - Clean dataset
- `POST /api/data/feature-engineering` - Apply feature engineering

### Machine Learning
- `POST /api/ml/train` - Train ML models
- `POST /api/ml/predict` - Make single predictions
- `POST /api/ml/batch-predict` - Make batch predictions
- `GET /api/models/available` - Get available models

### Visualization
- `GET /api/visualization/correlation` - Get correlation matrix
- `GET /api/visualization/distribution/{column}` - Get distribution data
- `GET /api/map/data` - Get map visualization data

### Export
- `POST /api/export` - Export processed data

## Features

- CSV data upload and parsing
- Data cleaning and preprocessing
- Feature engineering
- Multiple ML model training (Linear Regression, Random Forest, Decision Tree, etc.)
- Model evaluation and comparison
- Predictions (single and batch)
- Data visualization support
- Map data extraction
- Export functionality
