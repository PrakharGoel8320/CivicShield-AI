"""
CivicShield AI - IoT Sensor Data Collector Example

This script demonstrates how to collect data from multiple sources
(IoT sensors, APIs, satellites, etc.) and automatically upload to CivicShield AI.

Real-world scenario: Smart City Crime Prevention System
- Collects data from various sources
- Aggregates into unified CSV format
- Automatically uploads for ML processing
- Triggers model retraining periodically

Adapt this template to your specific data sources and use case.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Any
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SensorDataCollector:
    """
    Collects data from multiple sources and uploads to CivicShield AI
    
    Example sources:
    - IoT sensors (temperature, humidity, air quality)
    - Weather APIs
    - Traffic sensors
    - Satellite data
    - Government open data APIs
    - Social media APIs
    """
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.data_buffer = []
        self.last_upload_time = datetime.now()
        self.upload_interval = timedelta(minutes=15)  # Upload every 15 minutes
        
    # ============== DATA COLLECTION METHODS ==============
    
    def collect_iot_sensor_data(self) -> Dict[str, Any]:
        """
        Collect data from IoT sensors (temperature, humidity, etc.)
        
        In production, replace with actual sensor API calls:
        - MQTT broker for IoT devices
        - RESTful APIs from sensor manufacturers
        - Serial communication for local sensors
        """
        # SIMULATION - Replace with actual API calls
        return {
            'sensor_type': 'environmental',
            'temperature': 22.5 + (datetime.now().second % 10),
            'humidity': 55 + (datetime.now().second % 20),
            'air_quality_pm25': 15 + (datetime.now().second % 30),
            'noise_level_db': 60 + (datetime.now().second % 25)
        }
    
    def collect_weather_data(self) -> Dict[str, Any]:
        """
        Collect weather data from APIs
        
        Production APIs:
        - OpenWeatherMap: https://openweathermap.org/api
        - Weather.gov: https://www.weather.gov/documentation/services-web-api
        - AccuWeather: https://developer.accuweather.com/
        """
        # EXAMPLE - Using OpenWeatherMap (requires API key)
        # api_key = "YOUR_API_KEY"
        # url = f"https://api.openweathermap.org/data/2.5/weather?q=San Francisco&appid={api_key}"
        # response = requests.get(url)
        # data = response.json()
        
        # SIMULATION
        return {
            'weather_temp': 18.5,
            'weather_humidity': 65,
            'weather_wind_speed': 12.5,
            'weather_precipitation': 0.0,
            'weather_condition': 'Clear'
        }
    
    def collect_traffic_data(self) -> Dict[str, Any]:
        """
        Collect traffic data from sensors
        
        Production sources:
        - City traffic management APIs
        - Google Maps Traffic API
        - HERE Traffic API
        - Waze data feeds
        """
        # SIMULATION
        return {
            'traffic_volume': 450 + (datetime.now().minute * 10),
            'average_speed_mph': 35 + (datetime.now().second % 20),
            'congestion_level': 'moderate'
        }
    
    def collect_crime_data(self) -> Dict[str, Any]:
        """
        Collect crime statistics
        
        Production sources:
        - Police department APIs
        - 911 call center databases
        - Government open data portals (data.gov)
        - Crimemapping.com API
        """
        # SIMULATION
        return {
            'crime_incidents_24h': (datetime.now().day % 15),
            'emergency_calls_24h': (datetime.now().day % 25),
            'crime_type_majority': 'property'
        }
    
    def collect_satellite_data(self) -> Dict[str, Any]:
        """
        Collect satellite imagery data
        
        Production sources:
        - NASA EOSDIS: https://earthdata.nasa.gov/
        - Sentinel Hub: https://www.sentinel-hub.com/
        - Google Earth Engine: https://earthengine.google.com/
        - Planet Labs: https://www.planet.com/
        """
        # SIMULATION - Vegetation index, urban heat
        return {
            'vegetation_index_ndvi': 0.65,
            'urban_heat_celsius': 32.5,
            'cloud_cover_percent': 15
        }
    
    def collect_social_data(self) -> Dict[str, Any]:
        """
        Collect social media sentiment
        
        Production sources:
        - Twitter API: https://developer.twitter.com/
        - Reddit API: https://www.reddit.com/dev/api/
        - Facebook Graph API: https://developers.facebook.com/
        """
        # SIMULATION
        return {
            'social_sentiment_score': 0.65,  # -1 to 1 scale
            'post_count_24h': 150,
            'trending_topics': 'safety,community'
        }
    
    # ============== DATA AGGREGATION ==============
    
    def aggregate_data(self) -> Dict[str, Any]:
        """
        Combine all data sources into unified format
        This creates one row of data for the CSV
        """
        logger.info("🔄 Collecting data from all sources...")
        
        # Collect from all sources
        iot_data = self.collect_iot_sensor_data()
        weather_data = self.collect_weather_data()
        traffic_data = self.collect_traffic_data()
        crime_data = self.collect_crime_data()
        satellite_data = self.collect_satellite_data()
        social_data = self.collect_social_data()
        
        # Combine into single record
        unified_record = {
            'timestamp': datetime.now().isoformat(),
            'location_name': 'District_A',
            'latitude': 37.7749,
            'longitude': -122.4194,
            **iot_data,
            **weather_data,
            **traffic_data,
            **crime_data,
            **satellite_data,
            **social_data
        }
        
        logger.info(f"✅ Data collected: {len(unified_record)} fields")
        return unified_record
    
    # ============== UPLOAD LOGIC ==============
    
    def save_to_csv(self) -> str:
        """Save buffered data to CSV file"""
        if not self.data_buffer:
            return None
        
        df = pd.DataFrame(self.data_buffer)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data_to_upload/sensor_batch_{timestamp}.csv"
        
        # Create directory if it doesn't exist
        Path("data_to_upload").mkdir(exist_ok=True)
        
        df.to_csv(filename, index=False)
        logger.info(f"💾 Saved {len(self.data_buffer)} records to {filename}")
        
        return filename
    
    def upload_to_civicshield(self, csv_filename: str) -> bool:
        """Upload CSV file to CivicShield AI"""
        try:
            with open(csv_filename, 'rb') as f:
                files = {'file': (Path(csv_filename).name, f, 'text/csv')}
                response = requests.post(f"{self.api_url}/api/upload", files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Uploaded successfully: {data.get('total_rows')} rows, {data.get('columns')} columns")
                return True
            else:
                logger.error(f"❌ Upload failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Upload error: {str(e)}")
            return False
    
    def trigger_model_retraining(self):
        """
        Trigger automatic model retraining after accumulating enough new data
        
        In production:
        - Run weekly or when data drift detected
        - Use best hyperparameters from previous training
        - A/B test new model against old before deployment
        """
        logger.info("🧠 Triggering model retraining...")
        
        try:
            response = requests.post(f"{self.api_url}/api/ml/train", json={
                'target_column': 'crime_incidents_24h',  # What we want to predict
                'feature_columns': [
                    'temperature',
                    'humidity',
                    'traffic_volume',
                    'weather_temp',
                    'social_sentiment_score',
                    'vegetation_index_ndvi'
                ],
                'model_types': ['random_forest', 'gradient_boosting'],
                'test_size': 0.2
            }, timeout=120)
            
            if response.status_code == 200:
                results = response.json()
                logger.info(f"✅ Models trained successfully")
                for model in results.get('models', []):
                    logger.info(f"   {model['name']}: R² = {model['metrics'].get('r2_score', 'N/A')}")
            else:
                logger.error(f"❌ Training failed: {response.status_code}")
        
        except Exception as e:
            logger.error(f"❌ Training error: {str(e)}")
    
    # ============== MAIN COLLECTION LOOP ==============
    
    def run(self, collection_interval: int = 60, retrain_interval_hours: int = 24):
        """
        Main data collection loop
        
        Args:
            collection_interval: Seconds between data collections (default: 60)
            retrain_interval_hours: Hours between model retraining (default: 24)
        """
        logger.info("=" * 70)
        logger.info("🚀 CivicShield AI - Sensor Data Collector Started")
        logger.info("=" * 70)
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Collection interval: {collection_interval} seconds")
        logger.info(f"Upload interval: {self.upload_interval.total_seconds() / 60} minutes")
        logger.info(f"Retrain interval: {retrain_interval_hours} hours")
        logger.info("")
        
        last_retrain = datetime.now()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                logger.info(f"\n{'=' * 70}")
                logger.info(f"Iteration #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'=' * 70}")
                
                # Collect data
                data_record = self.aggregate_data()
                self.data_buffer.append(data_record)
                
                # Check if it's time to upload
                if datetime.now() - self.last_upload_time >= self.upload_interval:
                    logger.info(f"\n📤 Upload time reached ({len(self.data_buffer)} records buffered)")
                    
                    # Save to CSV
                    csv_file = self.save_to_csv()
                    
                    if csv_file:
                        # Upload to CivicShield AI
                        if self.upload_to_civicshield(csv_file):
                            self.data_buffer = []  # Clear buffer after successful upload
                            self.last_upload_time = datetime.now()
                
                # Check if it's time to retrain models
                hours_since_retrain = (datetime.now() - last_retrain).total_seconds() / 3600
                if hours_since_retrain >= retrain_interval_hours:
                    logger.info(f"\n🔄 Retraining time reached ({hours_since_retrain:.1f} hours)")
                    self.trigger_model_retraining()
                    last_retrain = datetime.now()
                
                # Wait before next collection
                logger.info(f"\n💤 Waiting {collection_interval} seconds until next collection...")
                time.sleep(collection_interval)
        
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Collector stopped by user")
            
            # Save any remaining data before exit
            if self.data_buffer:
                logger.info("💾 Saving remaining buffered data...")
                csv_file = self.save_to_csv()
                if csv_file:
                    self.upload_to_civicshield(csv_file)
        
        except Exception as e:
            logger.error(f"\n💥 Unexpected error: {str(e)}")
            raise


def main():
    """
    Main entry point - customize as needed
    """
    # Configuration
    API_URL = "http://localhost:8000"
    COLLECTION_INTERVAL = 60  # Collect data every 60 seconds
    RETRAIN_INTERVAL_HOURS = 24  # Retrain models every 24 hours
    
    # Create and run collector
    collector = SensorDataCollector(api_url=API_URL)
    collector.run(
        collection_interval=COLLECTION_INTERVAL,
        retrain_interval_hours=RETRAIN_INTERVAL_HOURS
    )


if __name__ == "__main__":
    main()
