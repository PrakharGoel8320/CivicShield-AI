"""
Fully Automated ML Pipeline
Monitors for data -> Auto-detects target/features -> Trains models -> Predicts -> Sends alerts

This is the main automation service that runs continuously
"""

import requests
import pandas as pd
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
import sys
import json
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AutomatedPipeline:
    """
    Fully automated ML pipeline that:
    1. Monitors folder for new sensor data CSV files
    2. Automatically detects target column and features
    3. Uploads data to backend
    4. Trains best models automatically
    5. Makes predictions on new data
    6. Sends alerts based on predictions
    7. Stores results back to CSV
    """
    
    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        watch_folder: str = "sensor_data",
        output_folder: str = "prediction_results",
        check_interval: int = 30,
        auto_train: bool = True,
        alert_thresholds: Optional[Dict] = None
    ):
        self.api_url = api_url
        self.watch_folder = Path(watch_folder)
        self.output_folder = Path(output_folder)
        self.check_interval = check_interval
        self.auto_train = auto_train
        self.alert_thresholds = alert_thresholds or {}
        
        # Create folders
        self.watch_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        
        # Track processed files
        self.processed_files = set()
        self.trained_models = {}  # dataset -> model info
        
        logger.info("=" * 80)
        logger.info("🚀 CivicShield AI - Automated Pipeline Started")
        logger.info("=" * 80)
        logger.info(f"📁 Watching folder: {self.watch_folder.absolute()}")
        logger.info(f"📂 Output folder: {self.output_folder.absolute()}")
        logger.info(f"🌐 API URL: {self.api_url}")
        logger.info(f"⏱️  Check interval: {self.check_interval}s")
        logger.info(f"🤖 Auto-train: {self.auto_train}")
        logger.info("=" * 80)
    
    def check_api_health(self) -> bool:
        """Check if backend API is accessible"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"❌ API not accessible: {e}")
            return False
    
    def upload_dataset(self, file_path: Path) -> Optional[Dict]:
        """Upload CSV dataset to backend"""
        try:
            logger.info(f"📤 Uploading: {file_path.name}")
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'text/csv')}
                response = requests.post(
                    f"{self.api_url}/api/upload",
                    files=files,
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Upload successful")
                logger.info(f"   Rows: {data.get('rows')}, Columns: {data.get('columns')}")
                return data
            else:
                logger.error(f"❌ Upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error uploading {file_path.name}: {e}")
            return None
    
    def auto_detect_and_train(self, dataset_info: Dict) -> Optional[Dict]:
        """Automatically detect target/features and train models"""
        try:
            dataset_name = dataset_info['dataset_name']
            logger.info(f"🔍 Auto-detecting target and features for: {dataset_name}")
            
            # Call auto-detection endpoint
            response = requests.post(
                f"{self.api_url}/api/ml/auto-train",
                json={
                    'dataset_name': dataset_name,
                    'enable_auto_detect': True
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Auto-training complete!")
                logger.info(f"   Target: {result.get('target')}")
                logger.info(f"   Features: {len(result.get('features', []))}")
                logger.info(f"   Best Model: {result.get('best_model')}")
                logger.info(f"   Best Accuracy: {result.get('best_accuracy', 0):.2%}")
                return result
            else:
                logger.error(f"❌ Auto-training failed: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error in auto-training: {e}")
            return None
    
    def make_predictions(
        self,
        dataset_name: str,
        target: str,
        model_name: str,
        data: pd.DataFrame
    ) -> Optional[pd.DataFrame]:
        """Make predictions on new data"""
        try:
            logger.info(f"🎯 Making predictions with {model_name}...")
            
            # Prepare prediction data
            predictions = []
            alerts = []
            
            for idx, row in data.iterrows():
                # Convert row to dict, excluding target if present
                input_data = row.to_dict()
                if target in input_data:
                    del input_data[target]
                
                # Make prediction
                response = requests.post(
                    f"{self.api_url}/api/ml/predict",
                    json={
                        'dataset_name': dataset_name,
                        'target': target,
                        'model_name': model_name,
                        'input_data': input_data
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result['prediction']
                    predictions.append(prediction)
                    
                    # Check if alert needed
                    alert = self.check_alert_threshold(target, prediction, input_data)
                    if alert:
                        alerts.append(alert)
                        self.send_alert(alert)
                else:
                    predictions.append(None)
            
            # Add predictions to dataframe
            data[f'{target}_prediction'] = predictions
            data['prediction_timestamp'] = datetime.now().isoformat()
            
            logger.info(f"✅ Predictions complete: {len(predictions)} rows")
            if alerts:
                logger.warning(f"🚨 {len(alerts)} alerts triggered!")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error making predictions: {e}")
            return None
    
    def check_alert_threshold(
        self,
        target: str,
        prediction: float,
        input_data: Dict
    ) -> Optional[Dict]:
        """Check if prediction exceeds alert threshold"""
        
        # Default thresholds
        default_thresholds = {
            'flood_risk_level': 4,
            'waterlogging_risk': 4,
            'aqi_value': 150,
            'congestion_level': 4,
            'crime_incidents': 5,
            'pothole_severity': 4,
            'road_damage_level': 4,
            'diversion_needed': 1
        }
        
        threshold = self.alert_thresholds.get(target, default_thresholds.get(target, 4))
        
        if prediction >= threshold:
            severity = 'HIGH' if prediction >= threshold + 1 else 'MEDIUM'
            
            return {
                'timestamp': datetime.now().isoformat(),
                'severity': severity,
                'target': target,
                'predicted_value': prediction,
                'threshold': threshold,
                'input_data': input_data
            }
        
        return None
    
    def send_alert(self, alert: Dict):
        """Log alert (can be extended to send emails, SMS, etc.)"""
        severity_icon = '🔴' if alert['severity'] == 'HIGH' else '🟡'
        
        logger.warning("=" * 80)
        logger.warning(f"{severity_icon} ALERT - {alert['severity']}")
        logger.warning(f"Target: {alert['target']}")
        logger.warning(f"Predicted Value: {alert['predicted_value']:.2f} (Threshold: {alert['threshold']})")
        logger.warning(f"Timestamp: {alert['timestamp']}")
        logger.warning(f"Input Data: {json.dumps(alert['input_data'], indent=2)}")
        logger.warning("=" * 80)
        
        # Save alert to file
        alert_file = self.output_folder / "alerts.jsonl"
        with open(alert_file, 'a') as f:
            f.write(json.dumps(alert) + '\n')
    
    def save_results(self, data: pd.DataFrame, original_file: Path):
        """Save prediction results to output folder"""
        try:
            output_file = self.output_folder / f"{original_file.stem}_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            data.to_csv(output_file, index=False)
            logger.info(f"💾 Results saved: {output_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")
            return None
    
    def process_file(self, file_path: Path):
        """Complete processing pipeline for a single file"""
        try:
            logger.info("=" * 80)
            logger.info(f"🔄 Processing: {file_path.name}")
            logger.info("=" * 80)
            
            # 1. Upload dataset
            dataset_info = self.upload_dataset(file_path)
            if not dataset_info:
                logger.error("Failed to upload dataset")
                return
            
            dataset_name = dataset_info['dataset_name']
            
            # 2. Auto-detect and train models
            if self.auto_train:
                training_result = self.auto_detect_and_train(dataset_info)
                if not training_result:
                    logger.error("Failed to train models")
                    return
                
                target = training_result['target']
                best_model = training_result['best_model']
                
                self.trained_models[dataset_name] = {
                    'target': target,
                    'model': best_model,
                    'accuracy': training_result.get('best_accuracy'),
                    'features': training_result.get('features', [])
                }
            else:
                logger.info("⏭️  Skipping training (auto_train=False)")
                return
            
            # 3. Load original data and make predictions
            data = pd.read_csv(file_path)
            predictions_df = self.make_predictions(
                dataset_name,
                target,
                best_model,
                data
            )
            
            if predictions_df is not None:
                # 4. Save results
                self.save_results(predictions_df, file_path)
            
            # 5. Mark as processed
            self.processed_files.add(str(file_path))
            
            logger.info("=" * 80)
            logger.info(f"✅ Processing complete: {file_path.name}")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"❌ Error processing {file_path.name}: {e}", exc_info=True)
    
    def scan_for_new_files(self):
        """Scan watch folder for new CSV files"""
        csv_files = list(self.watch_folder.glob("*.csv"))
        
        new_files = []
        for file_path in csv_files:
            if str(file_path) not in self.processed_files:
                new_files.append(file_path)
        
        return new_files
    
    def run(self):
        """Main loop - continuously monitor and process files"""
        logger.info("👀 Starting file monitoring...")
        
        while True:
            try:
                # Check API health
                if not self.check_api_health():
                    logger.warning("⚠️  Backend API not accessible, retrying in 30s...")
                    time.sleep(30)
                    continue
                
                # Scan for new files
                new_files = self.scan_for_new_files()
                
                if new_files:
                    logger.info(f"📋 Found {len(new_files)} new file(s)")
                    
                    for file_path in new_files:
                        self.process_file(file_path)
                        
                        # Small delay between files
                        time.sleep(2)
                else:
                    # No new files
                    logger.debug(f"No new files. Next check in {self.check_interval}s...")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("\n🛑 Stopping automation service...")
                break
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}", exc_info=True)
                time.sleep(self.check_interval)


def main():
    """Main entry point"""
    import argparse
    
    # Get default API URL from environment variable or use localhost
    default_api_url = os.getenv('BACKEND_URL', os.getenv('API_URL', 'http://localhost:8000'))
    
    parser = argparse.ArgumentParser(description='CivicShield AI - Automated ML Pipeline')
    parser.add_argument('--api-url', default=default_api_url, help='Backend API URL (or set BACKEND_URL env var)')
    parser.add_argument('--watch-folder', default='sensor_data', help='Folder to monitor for CSV files')
    parser.add_argument('--output-folder', default='prediction_results', help='Folder for prediction results')
    parser.add_argument('--interval', type=int, default=30, help='Check interval in seconds')
    parser.add_argument('--no-train', action='store_true', help='Disable automatic training')
    
    args = parser.parse_args()
    
    pipeline = AutomatedPipeline(
        api_url=args.api_url,
        watch_folder=args.watch_folder,
        output_folder=args.output_folder,
        check_interval=args.interval,
        auto_train=not args.no_train
    )
    
    pipeline.run()


if __name__ == '__main__':
    main()
