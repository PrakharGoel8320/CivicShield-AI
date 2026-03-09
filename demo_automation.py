"""
Quick Start - Automated Pipeline Demo
Run this to test the automation system
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Create demo sensor data folder
sensor_data_folder = Path("sensor_data")
sensor_data_folder.mkdir(exist_ok=True)

print("=" * 80)
print("🚀 CivicShield AI - Automation Demo")
print("=" * 80)
print("\n📝 Generating sample sensor data...\n")

# Generate sample pothole detection data
np.random.seed(42)
n_samples = 30

pothole_data = pd.DataFrame({
    'road_segment_id': [f'RS_{i:03d}' for i in range(1, n_samples + 1)],
    'latitude': np.random.uniform(37.75, 37.80, n_samples),
    'longitude': np.random.uniform(-122.45, -122.40, n_samples),
    'vibration_intensity': np.random.uniform(1.5, 5.5, n_samples),
    'surface_roughness_mm': np.random.uniform(3, 22, n_samples),
    'crack_width_mm': np.random.uniform(0.5, 6.5, n_samples),
    'depression_depth_mm': np.random.uniform(5, 75, n_samples),
    'vehicle_speed_kmh': np.random.uniform(25, 60, n_samples),
    'sensor_confidence': np.random.uniform(0.80, 0.98, n_samples),
    'weather_condition': np.random.choice(['dry', 'wet'], n_samples),
    'previous_reports': np.random.randint(0, 7, n_samples),
    'maintenance_age_days': np.random.randint(30, 900, n_samples),
    'traffic_volume': np.random.randint(3000, 14000, n_samples),
})

# Calculate severity based on features (realistic correlation)
pothole_data['pothole_severity'] = (
    (pothole_data['vibration_intensity'] * 0.4) +
    (pothole_data['depression_depth_mm'] / 20) +
    (pothole_data['crack_width_mm'] * 0.3) +
    (pothole_data['previous_reports'] * 0.2)
).round().clip(1, 5).astype(int)

# Save to sensor_data folder
output_file = sensor_data_folder / f"pothole_sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
pothole_data.to_csv(output_file, index=False)

print(f"✅ Generated: {output_file.name}")
print(f"   Samples: {len(pothole_data)}")
print(f"   Columns: {len(pothole_data.columns)}")
print(f"\n📊 Sample data:")
print(pothole_data[['road_segment_id', 'vibration_intensity', 'depression_depth_mm', 'pothole_severity']].head())

print("\n" + "=" * 80)
print("🎯 Next Steps:")
print("=" * 80)
print("\n1. Start the backend:")
print("   cd backend")
print("   python main.py")
print("\n2. Start the automation pipeline:")
print("   python automated_pipeline.py")
print("\n3. Watch the magic happen! The pipeline will:")
print("   ✅ Detect the new CSV file")
print("   ✅ Upload to backend")
print("   ✅ Auto-detect target (pothole_severity) and features")
print("   ✅ Train best ML models (Random Forest, Gradient Boosting)")
print("   ✅ Make predictions on all rows")
print("   ✅ Trigger alerts for severity >= 4")
print("   ✅ Save results to prediction_results/ folder")
print("\n4. Monitor logs:")
print("   tail -f automation.log")
print("   tail -f alerts.log")
print("\n" + "=" * 80)
print("💡 Tip: Add more CSV files to sensor_data/ folder")
print("         The automation will process them automatically!")
print("=" * 80)
