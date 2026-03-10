"""
CivicShield AI - Backend API Server
FastAPI backend for data processing, ML model training, and predictions
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
import numpy as np
import io
import json
from typing import List, Dict, Any, Optional
import joblib
import os
import logging
from datetime import datetime

from models.ml_models import MLModelTrainer
from utils.data_preprocessing import DataPreprocessor
from utils.feature_engineering import FeatureEngineer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CivicShield AI API",
    description="Backend API for CivicShield AI - Urban Solutions Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for datasets and models
current_dataset = None
uploaded_datasets: Dict[str, pd.DataFrame] = {}
dataset_upload_order: List[str] = []
trained_models = {}
trained_model_metadata = {}
preprocessing_pipeline = None

# Recommended target->feature mapping used across training UI/API.
TARGET_FEATURE_MAPPING: Dict[str, List[str]] = {
    "flood_risk_level": ["rainfall_mm", "river_level_m", "soil_moisture_percent", "temperature_c", "wind_speed_kmh", "previous_flood_count", "elevation_m", "drainage_capacity_percent", "population_density"],
    "aqi_value": ["pm25", "pm10", "no2", "so2", "co", "o3", "temperature_c", "humidity_percent", "wind_speed_kmh", "traffic_volume"],
    "congestion_level": ["vehicle_count", "average_speed_kmh", "incident_count", "temperature_c", "hour_of_day"],
    "waste_per_capita_kg": ["household_count", "waste_collected_kg", "recyclable_kg", "organic_kg", "hazardous_kg", "population", "bins_overflowing"],
    "waterlogging_risk": ["rainfall_mm", "drainage_capacity_percent", "previous_incidents", "elevation_m", "pump_stations_active", "water_level_cm"],
    "crime_incidents": ["population", "police_per_1000", "unemployment_rate", "avg_income", "education_high_school_percent", "street_lights_working_percent", "cctv_cameras", "previous_crimes_30d", "temperature_c"],
    "energy_consumption_kwh": ["floor_area_sqm", "occupancy_count", "hvac_efficiency", "temperature_c"],
    "ridership_count": ["hour", "temperature_c", "fuel_price"],
}


def get_dataset(dataset_name: Optional[str] = None) -> pd.DataFrame:
    """Resolve a dataset by name, defaulting to the latest uploaded dataset."""
    global current_dataset, uploaded_datasets, dataset_upload_order

    if dataset_name:
        if dataset_name not in uploaded_datasets:
            raise HTTPException(status_code=404, detail=f"Dataset not found: {dataset_name}")
        return uploaded_datasets[dataset_name]

    if dataset_upload_order:
        latest_name = dataset_upload_order[-1]
        return uploaded_datasets[latest_name]

    if current_dataset is not None:
        return current_dataset

    raise HTTPException(status_code=404, detail="No dataset uploaded")


def build_model_id(dataset_name: Optional[str], target: str, model_name: str) -> str:
    """Create a stable model identifier so models from different datasets/targets don't collide."""
    dataset_part = dataset_name or "latest_dataset"
    return f"{dataset_part}::{target}::{model_name}"


def make_json_serializable(obj: Any) -> Any:
    """Convert numpy/pandas objects to plain Python types for FastAPI responses."""
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_serializable(v) for v in obj]
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if isinstance(obj, (pd.Series, pd.Index)):
        return obj.tolist()
    return obj


def build_feature_profiles(X: pd.DataFrame, features: List[str]) -> Dict[str, Dict[str, Any]]:
    """Build simple feature stats used for prediction defaults and range checks."""
    stats: Dict[str, Dict[str, Any]] = {}
    dtypes: Dict[str, str] = {}

    for feature in features:
        series = X[feature]
        dtypes[feature] = str(series.dtype)
        if pd.api.types.is_numeric_dtype(series):
            stats[feature] = {
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
                "median": float(series.median()),
            }

    return {"feature_stats": stats, "feature_dtypes": dtypes}

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "CivicShield AI API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload and parse CSV dataset
    Returns basic dataset information and preview
    """
    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Store dataset globally (latest + full dataset registry)
        global current_dataset, uploaded_datasets, dataset_upload_order
        current_dataset = df
        dataset_name = file.filename or f"dataset_{len(dataset_upload_order) + 1}.csv"
        uploaded_datasets[dataset_name] = df
        if dataset_name in dataset_upload_order:
            dataset_upload_order.remove(dataset_name)
        dataset_upload_order.append(dataset_name)
        
        # Generate dataset statistics
        stats = {
            "filename": file.filename,
            "dataset_name": dataset_name,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "column_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "preview": df.head(10).to_dict(orient="records"),
            "numerical_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=["object", "string", "category"]).columns.tolist(),
        }
        
        # Add summary statistics for numerical columns
        if len(stats["numerical_columns"]) > 0:
            stats["numerical_stats"] = df[stats["numerical_columns"]].describe().to_dict()
        
        return JSONResponse(content=make_json_serializable(stats))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.get("/api/datasets")
async def list_uploaded_datasets():
    """List all uploaded datasets with basic metadata."""
    global uploaded_datasets, dataset_upload_order

    datasets = []
    for name in dataset_upload_order:
        df = uploaded_datasets[name]
        datasets.append({
            "dataset_name": name,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numerical_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
        })

    return {"datasets": make_json_serializable(datasets)}


@app.get("/api/ml/target-options")
async def get_target_options():
    """Return available target columns from all uploaded datasets with mapped features."""
    global uploaded_datasets, dataset_upload_order

    if not dataset_upload_order:
        raise HTTPException(status_code=404, detail="No dataset uploaded")

    options = []
    for dataset_name in dataset_upload_order:
        df = uploaded_datasets[dataset_name]
        columns = set(df.columns.tolist())
        numeric_cols = set(df.select_dtypes(include=[np.number]).columns.tolist())

        for target, mapped_features in TARGET_FEATURE_MAPPING.items():
            if target in columns:
                available_features = [f for f in mapped_features if f in numeric_cols and f in columns and f != target]
                options.append({
                    "id": f"{dataset_name}::{target}",
                    "dataset_name": dataset_name,
                    "target_column": target,
                    "feature_columns": available_features,
                })

    return {"target_options": make_json_serializable(options)}


@app.get("/api/data/preview")
async def get_data_preview(limit: int = 100, dataset_name: str = None):
    """Get current dataset preview"""
    current = get_dataset(dataset_name)

    return {
        "data": current.head(limit).to_dict(orient="records"),
        "total_rows": len(current),
        "dataset_name": dataset_name,
    }

@app.get("/api/data/statistics")
async def get_statistics(dataset_name: str = None):
    """Get comprehensive dataset statistics"""
    df = get_dataset(dataset_name)
    numerical_df = df.select_dtypes(include=[np.number])
    row_count = len(df)
    missing_values = df.isnull().sum()
    
    stats = {
        "basic_info": {
            "total_rows": row_count,
            "total_columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum() / 1024**2,  # MB
            "duplicates": df.duplicated().sum()
        },
        "numerical_summary": numerical_df.describe().to_dict() if not numerical_df.empty else {},
        "missing_values": missing_values.to_dict(),
        "missing_percentage": ((missing_values / row_count) * 100).to_dict() if row_count > 0 else {},
        "column_types": df.dtypes.astype(str).to_dict(),
    }
    
    return make_json_serializable(stats)

@app.post("/api/data/clean")
async def clean_data(options: Dict[str, Any]):
    """
    Clean dataset based on provided options
    Options: handle_missing, remove_duplicates, outliers_removal
    """
    global current_dataset, preprocessing_pipeline, uploaded_datasets
    dataset_name = options.get("dataset_name")
    df = get_dataset(dataset_name).copy()
    preprocessor = DataPreprocessor()
    
    try:
        # Handle missing values
        if options.get("handle_missing"):
            method = options.get("missing_method", "mean")
            df = preprocessor.handle_missing_values(df, method=method)
        
        # Remove duplicates
        if options.get("remove_duplicates"):
            df = preprocessor.remove_duplicates(df)
        
        # Handle outliers
        if options.get("remove_outliers"):
            df = preprocessor.handle_outliers(df)
        
        # Update selected dataset + latest pointer
        current_dataset = df
        if dataset_name and dataset_name in uploaded_datasets:
            uploaded_datasets[dataset_name] = df
        
        return {
            "message": "Data cleaned successfully",
            "rows_after_cleaning": len(df),
            "columns_after_cleaning": len(df.columns)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error cleaning data: {str(e)}")

@app.post("/api/data/feature-engineering")
async def feature_engineering(config: Dict[str, Any]):
    """Apply feature engineering techniques"""
    global current_dataset, uploaded_datasets
    dataset_name = config.get("dataset_name")
    
    engineer = FeatureEngineer()
    df = get_dataset(dataset_name).copy()
    
    try:
        # Create date features if date columns exist
        if config.get("create_date_features"):
            date_columns = config.get("date_columns", [])
            for col in date_columns:
                if col in df.columns:
                    df = engineer.create_date_features(df, col)
        
        # Create polynomial features
        if config.get("polynomial_features"):
            feature_cols = config.get("feature_columns", [])
            degree = config.get("degree", 2)
            df = engineer.create_polynomial_features(df, feature_cols, degree)
        
        current_dataset = df
        if dataset_name and dataset_name in uploaded_datasets:
            uploaded_datasets[dataset_name] = df
        
        return {
            "message": "Feature engineering completed",
            "new_columns": len(df.columns),
            "column_names": df.columns.tolist()
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in feature engineering: {str(e)}")

@app.post("/api/ml/train")
async def train_model(config: Dict[str, Any]):
    """
    Train machine learning models
    Config includes: target_column, feature_columns, model_types, test_size
    """
    global current_dataset, trained_models, trained_model_metadata
    
    try:
        target = config.get("target_column")
        features = config.get("feature_columns")
        dataset_name = config.get("dataset_name")
        model_types = config.get("model_types", ["random_forest"])
        test_size = config.get("test_size", 0.2)

        df_source = get_dataset(dataset_name)
        
        if not target or not features:
            raise HTTPException(status_code=400, detail="Target and feature columns required")

        # Validate columns explicitly for clearer error messages
        missing_features = [col for col in features if col not in df_source.columns]
        if missing_features:
            raise HTTPException(
                status_code=400,
                detail=f"Feature columns not found in dataset: {missing_features}"
            )

        if target not in df_source.columns:
            raise HTTPException(status_code=400, detail=f"Target column not found in dataset: {target}")
        
        # Prepare data
        df = df_source[features + [target]].dropna()
        X = df[features]
        y = df[target]
        feature_profiles = build_feature_profiles(X, features)
        
        # Initialize trainer
        trainer = MLModelTrainer()
        
        # Train models
        results = trainer.train_models(X, y, model_types, test_size)
        
        # Store trained models without wiping previous dataset/target trainings.
        trained_now = results["models"]
        needs_scaling = results.get("needs_scaling", {})
        scaler = results.get("scaler")
        
        # Prepare response
        response = {
            "message": "Models trained successfully",
            "models": []
        }
        
        for model_name, metrics in results["metrics"].items():
            model_id = build_model_id(dataset_name, target, model_name)
            
            # Store model with scaler as a dict
            trained_models[model_id] = {
                "model": trained_now[model_name],
                "scaler": scaler,
                "needs_scaling": needs_scaling.get(model_name, False)
            }
            
            trained_model_metadata[model_id] = {
                "model_id": model_id,
                "model_name": model_name,
                "feature_columns": features,
                "needs_scaling": needs_scaling.get(model_name, False),
                "feature_stats": feature_profiles["feature_stats"],
                "feature_dtypes": feature_profiles["feature_dtypes"],
                "target_column": target,
                "dataset_name": dataset_name,
                "metrics": metrics,
                "trained_at": datetime.now().isoformat()
            }
            response["models"].append({
                "model_id": model_id,
                "name": model_name,
                "metrics": metrics,
                "feature_importance": results.get("feature_importance", {}).get(model_name, {}),
                "feature_columns": features,
                "target_column": target,
                "dataset_name": dataset_name,
                "feature_stats": feature_profiles["feature_stats"],
                "feature_dtypes": feature_profiles["feature_dtypes"],
            })
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error training models: {str(e)}")

@app.post("/api/ml/predict")
async def make_predictions(data: Dict[str, Any]):
    """
    Make predictions using trained model
    """
    global trained_models, trained_model_metadata
    
    if not trained_models:
        raise HTTPException(status_code=404, detail="No trained models available")
    
    try:
        model_id = data.get("model_id")
        model_name = data.get("model_name")
        input_data = data.get("input_data", {})

        resolved_model_id = None
        if model_id:
            resolved_model_id = model_id
        elif model_name:
            # Backward compatibility path: exact ID match if older clients send model_name.
            if model_name in trained_models:
                resolved_model_id = model_name
            else:
                # Try resolve by algorithm name when unique.
                matches = [mid for mid, meta in trained_model_metadata.items() if meta.get("model_name") == model_name]
                if len(matches) == 1:
                    resolved_model_id = matches[0]
                elif len(matches) > 1:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Multiple trained models found for algorithm '{model_name}'. "
                            "Please pass model_id instead."
                        )
                    )

        if not resolved_model_id or resolved_model_id not in trained_models:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id or model_name}")

        model_meta = trained_model_metadata.get(resolved_model_id, {})
        required_features = model_meta.get("feature_columns", [])
        feature_stats = model_meta.get("feature_stats", {})
        feature_dtypes = model_meta.get("feature_dtypes", {})

        if not required_features:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"No stored feature schema for model '{resolved_model_id}'. "
                    "Please retrain the model and try again."
                )
            )

        missing_features = [f for f in required_features if f not in input_data]
        if missing_features:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Missing required features for model '{model_name}': {missing_features}. "
                    f"Required feature names: {required_features}"
                )
            )

        # Parse and validate inputs against training distribution.
        ordered_input = {}
        warnings = []
        for feature in required_features:
            raw_value = input_data[feature]
            dtype = feature_dtypes.get(feature, "")
            numeric_expected = feature in feature_stats or any(k in dtype for k in ["int", "float"])

            if numeric_expected:
                try:
                    value = float(raw_value)
                except (TypeError, ValueError):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Feature '{feature}' must be numeric. Received: {raw_value}"
                    )

                stats = feature_stats.get(feature)
                if stats:
                    if value < stats["min"] or value > stats["max"]:
                        warnings.append(
                            f"Feature '{feature}' is outside training range [{stats['min']:.3f}, {stats['max']:.3f}]"
                        )
                ordered_input[feature] = value
            else:
                ordered_input[feature] = raw_value
        
        # Convert input to DataFrame
        df_input = pd.DataFrame([ordered_input])
        
        # Get model and scaler
        model_data = trained_models[resolved_model_id]
        
        # Handle both old format (direct model) and new format (dict with model/scaler)
        if isinstance(model_data, dict):
            model = model_data["model"]
            scaler = model_data.get("scaler")
            needs_scaling = model_data.get("needs_scaling", False)
        else:
            # Backward compatibility for old stored models
            model = model_data
            scaler = None
            needs_scaling = False
        
        # Apply scaling if needed (for SVM, Logistic Regression models)
        if needs_scaling and scaler is not None:
            df_input_scaled = pd.DataFrame(
                scaler.transform(df_input),
                columns=df_input.columns,
                index=df_input.index
            )
            predictions = model.predict(df_input_scaled)
        else:
            predictions = model.predict(df_input)
        
        # Get prediction probabilities if classifier
        probabilities = None
        if hasattr(model, "predict_proba"):
            if needs_scaling and scaler is not None:
                probabilities = model.predict_proba(df_input_scaled).tolist()
            else:
                probabilities = model.predict_proba(df_input).tolist()
        
        return {
            "predictions": predictions.tolist(),
            "probabilities": probabilities,
            "model_used": model_meta.get("model_name", resolved_model_id),
            "model_id": resolved_model_id,
            "required_features": required_features,
            "target_column": model_meta.get("target_column"),
            "warnings": warnings,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error making predictions: {str(e)}")

@app.post("/api/ml/batch-predict")
async def batch_predictions(config: Dict[str, Any]):
    """Make predictions on entire dataset"""
    global trained_models
    
    if not trained_models:
        raise HTTPException(status_code=404, detail="No trained models available")
    
    try:
        model_id = config.get("model_id")
        model_name = config.get("model_name")
        feature_columns = config.get("feature_columns")
        dataset_name = config.get("dataset_name")
        df_source = get_dataset(dataset_name)

        resolved_model_id = model_id or model_name
        if not resolved_model_id or resolved_model_id not in trained_models:
            raise HTTPException(status_code=404, detail=f"Model not found: {model_id or model_name}")
        
        # Prepare data
        X = df_source[feature_columns].dropna()
        
        # Get model and scaler
        model_data = trained_models[resolved_model_id]
        
        # Handle both old format (direct model) and new format (dict with model/scaler)
        if isinstance(model_data, dict):
            model = model_data["model"]
            scaler = model_data.get("scaler")
            needs_scaling = model_data.get("needs_scaling", False)
        else:
            # Backward compatibility for old stored models
            model = model_data
            scaler = None
            needs_scaling = False
        
        # Make predictions with scaling if needed
        if needs_scaling and scaler is not None:
            X_scaled = pd.DataFrame(
                scaler.transform(X),
                columns=X.columns,
                index=X.index
            )
            predictions = model.predict(X_scaled)
        else:
            predictions = model.predict(X)
        
        return {
            "predictions": predictions.tolist(),
            "total_predictions": len(predictions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in batch predictions: {str(e)}")

@app.get("/api/visualization/correlation")
async def get_correlation_matrix(dataset_name: str = None):
    """Get correlation matrix for numerical columns"""
    df_source = get_dataset(dataset_name)

    # Get numerical columns
    numerical_df = df_source.select_dtypes(include=[np.number])
    
    if numerical_df.empty:
        raise HTTPException(status_code=400, detail="No numerical columns found")
    
    # Calculate correlation
    correlation = numerical_df.corr()
    
    return {
        "correlation": correlation.to_dict(),
        "columns": correlation.columns.tolist()
    }

@app.get("/api/visualization/distribution/{column}")
async def get_distribution(column: str, dataset_name: str = None):
    """Get distribution data for a specific column"""
    df_source = get_dataset(dataset_name)

    if column not in df_source.columns:
        raise HTTPException(status_code=404, detail=f"Column {column} not found")

    col_data = df_source[column].dropna()
    
    # Check if numerical or categorical
    if pd.api.types.is_numeric_dtype(col_data):
        # Create histogram bins
        hist, bins = np.histogram(col_data, bins=30)
        
        return {
            "type": "numerical",
            "hist": hist.tolist(),
            "bins": bins.tolist(),
            "stats": {
                "mean": float(col_data.mean()),
                "median": float(col_data.median()),
                "std": float(col_data.std()),
                "min": float(col_data.min()),
                "max": float(col_data.max())
            }
        }
    else:
        # Get value counts for categorical
        value_counts = col_data.value_counts().head(20)
        
        return {
            "type": "categorical",
            "categories": value_counts.index.tolist(),
            "counts": value_counts.values.tolist(),
            "unique_values": int(col_data.nunique())
        }

@app.get("/api/map/data")
async def get_map_data(lat_column: str = None, lon_column: str = None, dataset_name: str = None):
    """Get geographical data for map visualization"""
    df_source = get_dataset(dataset_name)
    
    # Auto-detect lat/lon columns if not provided
    if not lat_column or not lon_column:
        possible_lat = ['latitude', 'lat', 'Latitude', 'LAT']
        possible_lon = ['longitude', 'lon', 'lng', 'Longitude', 'LON']
        
        lat_column = next((col for col in df_source.columns if col in possible_lat), None)
        lon_column = next((col for col in df_source.columns if col in possible_lon), None)
    
    if not lat_column or not lon_column:
        raise HTTPException(status_code=404, detail="Lat/Lon columns not found")
    
    # Filter data with valid coordinates
    map_data = df_source[[lat_column, lon_column]].dropna()
    
    # Add additional columns if available
    extra_cols = [col for col in df_source.columns if col not in [lat_column, lon_column]]
    for col in extra_cols[:5]:  # Limit to 5 extra columns
        map_data[col] = df_source[col]
    
    return {
        "data": map_data.head(1000).to_dict(orient="records"),  # Limit to 1000 points
        "total_points": len(map_data),
        "lat_column": lat_column,
        "lon_column": lon_column
    }

@app.post("/api/export")
async def export_results(config: Dict[str, Any]):
    """Export processed data or predictions"""
    dataset_name = config.get("dataset_name")
    df_source = get_dataset(dataset_name)
    
    try:
        export_type = config.get("type", "csv")
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_type}"
        filepath = f"./exports/{filename}"
        
        # Create exports directory if not exists
        os.makedirs("./exports", exist_ok=True)
        
        # Export based on type
        if export_type == "csv":
            df_source.to_csv(filepath, index=False)
        elif export_type == "json":
            df_source.to_json(filepath, orient="records")
        elif export_type == "excel":
            df_source.to_excel(filepath, index=False)
        
        return {
            "message": "Export successful",
            "filename": filename,
            "path": filepath
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting data: {str(e)}")

@app.get("/api/models/available")
async def get_available_models():
    """Get list of available ML models"""
    return {
        "models": [
            {"name": "linear_regression", "type": "regression", "description": "Linear Regression"},
            {"name": "random_forest", "type": "both", "description": "Random Forest"},
            {"name": "decision_tree", "type": "both", "description": "Decision Tree"},
            {"name": "gradient_boosting", "type": "both", "description": "Gradient Boosting"},
            {"name": "svm", "type": "both", "description": "Support Vector Machine"}
        ]
    }


@app.get("/api/ml/trained-models")
async def get_trained_models():
    """Get trained models with required feature names for prediction UI."""
    global trained_models, trained_model_metadata

    models = []
    for model_id in trained_models.keys():
        meta = trained_model_metadata.get(model_id, {})
        models.append({
            "model_id": model_id,
            "name": meta.get("model_name", model_id),
            "feature_columns": meta.get("feature_columns", []),
            "target_column": meta.get("target_column"),
            "dataset_name": meta.get("dataset_name"),
            "metrics": meta.get("metrics", {}),
            "feature_stats": meta.get("feature_stats", {}),
            "feature_dtypes": meta.get("feature_dtypes", {}),
            "needs_scaling": meta.get("needs_scaling", False),
            "trained_at": meta.get("trained_at")
        })

    return {"models": make_json_serializable(models)}


@app.post("/api/ml/auto-train")
async def auto_train_models(config: Dict[str, Any]):
    """
    Automatically detect target/features and train best models
    
    Config:
        - dataset_name: Name of dataset
        - enable_auto_detect: If True, auto-detect target and features
        - max_features: Maximum number of features to select (optional)
        - model_types: List of models to try (optional)
    """
    global current_dataset, trained_models, trained_model_metadata
    
    try:
        dataset_name = config.get("dataset_name")
        enable_auto_detect = config.get("enable_auto_detect", True)
        max_features = config.get("max_features")
        model_types = config.get("model_types")
        test_size = config.get("test_size", 0.2)
        
        df_source = get_dataset(dataset_name)
        
        if enable_auto_detect:
            # Import intelligent detector
            from utils.intelligent_detector import IntelligentDetector
            
            logger.info("🔍 Starting intelligent auto-detection...")
            detector = IntelligentDetector()
            
            # Auto-detect target and features
            target, features = detector.auto_detect(df_source, max_features)
            
            # Get model recommendations if not specified
            if not model_types:
                model_types = detector.get_model_recommendations(df_source, target)
                logger.info(f"🤖 Using recommended models: {model_types}")
        else:
            # Manual specification required
            target = config.get("target_column")
            features = config.get("feature_columns")
            
            if not target or not features:
                raise HTTPException(
                    status_code=400,
                    detail="target_column and feature_columns required when auto_detect is disabled"
                )
            
            if not model_types:
                model_types = ["random_forest", "gradient_boosting", "decision_tree"]
        
        # Prepare data
        df = df_source[features + [target]].dropna()
        X = df[features]
        y = df[target]
        feature_profiles = build_feature_profiles(X, features)
        
        # Initialize trainer
        trainer = MLModelTrainer()
        
        # Train models
        logger.info(f"🏋️ Training {len(model_types)} models...")
        results = trainer.train_models(X, y, model_types, test_size)
        
        # Store trained models
        trained_now = results["models"]
        needs_scaling = results.get("needs_scaling", {})
        scaler = results.get("scaler")
        
        # Find best model based on accuracy
        best_model_name = None
        best_accuracy = 0
        
        for model_name, metrics in results["metrics"].items():
            accuracy = metrics.get("test_accuracy", metrics.get("test_r2", 0))
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model_name = model_name
        
        # Store all trained models
        response_models = []
        for model_name, metrics in results["metrics"].items():
            model_id = build_model_id(dataset_name, target, model_name)
            
            # Store model with scaler
            trained_models[model_id] = {
                "model": trained_now[model_name],
                "scaler": scaler,
                "needs_scaling": needs_scaling.get(model_name, False)
            }
            
            trained_model_metadata[model_id] = {
                "model_id": model_id,
                "model_name": model_name,
                "feature_columns": features,
                "needs_scaling": needs_scaling.get(model_name, False),
                "feature_stats": feature_profiles["feature_stats"],
                "feature_dtypes": feature_profiles["feature_dtypes"],
                "target_column": target,
                "dataset_name": dataset_name,
                "metrics": metrics,
                "trained_at": datetime.now().isoformat()
            }
            
            response_models.append({
                "model_id": model_id,
                "name": model_name,
                "metrics": metrics,
                "is_best": model_name == best_model_name
            })
        
        logger.info(f"✅ Auto-training complete! Best model: {best_model_name} ({best_accuracy:.2%})")
        
        return {
            "message": "Auto-training completed successfully",
            "target": target,
            "features": features,
            "num_features": len(features),
            "best_model": best_model_name,
            "best_accuracy": best_accuracy,
            "models": response_models,
            "dataset_name": dataset_name
        }
    
    except Exception as e:
        logger.error(f"❌ Error in auto-training: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error in auto-training: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
