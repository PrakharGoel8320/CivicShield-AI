# Training Checklist - Quick Reference

Print this or keep it open while training!

---

## ✅ Dataset 1: Flood Prediction
- [ ] Upload: `1_flood_prediction.csv`
- [ ] Check Analytics: rainfall range, elevation variations
- [ ] Target: `flood_risk_level`
- [ ] Features: `rainfall_mm`, `river_level_m`, `soil_moisture_percent`, `temperature_c`, `wind_speed_kmh`, `previous_flood_count`, `elevation_m`, `drainage_capacity_percent`, `population_density`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓, Decision Tree ✓
- [ ] Expected R²: 0.85-0.95
- [ ] Test Prediction (Level 5): rainfall_mm=95, river_level_m=8.5, soil_moisture_percent=98, temperature_c=22, wind_speed_kmh=35, previous_flood_count=4, elevation_m=7, drainage_capacity_percent=50, population_density=10000
- [ ] Expected Result: ~5.0 (Level 5 - severe flood risk)
- [ ] Test Prediction (Level 3): rainfall_mm=60, river_level_m=5.5, soil_moisture_percent=80, temperature_c=26, wind_speed_kmh=18, previous_flood_count=2, elevation_m=12, drainage_capacity_percent=75, population_density=6000
- [ ] Expected Result: ~3.0 (Level 3 - moderate risk)

---

## ✅ Dataset 2: Air Quality (AQI)
- [ ] Upload: `2_air_quality_prediction.csv`
- [ ] Check Analytics: PM2.5 and PM10 levels
- [ ] Target: `aqi_value`
- [ ] Features: `pm25`, `pm10`, `no2`, `so2`, `co`, `o3`, `temperature_c`, `humidity_percent`, `wind_speed_kmh`, `traffic_volume`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓
- [ ] Expected R²: 0.90-0.98
- [ ] Test Prediction: pm25=120, pm10=200, no2=85, so2=50, co=3.8, o3=18, temperature_c=22, humidity_percent=65, wind_speed_kmh=12, traffic_volume=4500
- [ ] Expected Result: AQI ~240-260 (Very Unhealthy)

---

## ✅ Dataset 3: Traffic Congestion
- [ ] Upload: `3_traffic_congestion.csv`
- [ ] Check Analytics: vehicle counts and speeds
- [ ] Target: `congestion_level`
- [ ] Features: `vehicle_count`, `average_speed_kmh`, `incident_count`, `temperature_c`, `hour_of_day`
- [ ] Models: Random Forest ✓, Decision Tree ✓
- [ ] Expected R²: 0.85-0.95
- [ ] Test Prediction: vehicle_count=7000, average_speed_kmh=12, incident_count=6, temperature_c=25, hour_of_day=17
- [ ] Expected Result: ~5.0 (Level 5 - severe congestion)

---

## ✅ Dataset 4: Waste Management
- [ ] Upload: `4_waste_management.csv`
- [ ] Check Analytics: waste per capita variations
- [ ] Target: `waste_per_capita_kg`
- [ ] Features: `household_count`, `waste_collected_kg`, `recyclable_kg`, `organic_kg`, `hazardous_kg`, `population`, `bins_overflowing`
- [ ] Models: Linear Regression ✓, Random Forest ✓
- [ ] Expected R²: 0.80-0.90
- [ ] Test Prediction: household_count=2500, waste_collected_kg=8500, recyclable_kg=1200, organic_kg=3500, hazardous_kg=150, population=8200, bins_overflowing=2
- [ ] Expected Result: ~1.03-1.06 kg/capita

---

## ✅ Dataset 5: Waterlogging
- [ ] Upload: `5_waterlogging_prediction.csv`
- [ ] Check Analytics: drainage capacity and rainfall
- [ ] Target: `waterlogging_risk`
- [ ] Features: `rainfall_mm`, `drainage_capacity_percent`, `previous_incidents`, `elevation_m`, `pump_stations_active`, `water_level_cm`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓
- [ ] Expected R²: 0.88-0.96
- [ ] Test Prediction: rainfall_mm=110, drainage_capacity_percent=45, previous_incidents=5, elevation_m=3, pump_stations_active=1, water_level_cm=57
- [ ] Expected Result: ~5.0 (Level 5 - severe waterlogging)

---

## ✅ Dataset 6: Crime Prediction
- [ ] Upload: `6_crime_prediction.csv`
- [ ] Check Analytics: unemployment and police ratios
- [ ] Target: `crime_incidents`
- [ ] Features: `population`, `police_per_1000`, `unemployment_rate`, `avg_income`, `education_high_school_percent`, `street_lights_working_percent`, `cctv_cameras`, `previous_crimes_30d`, `temperature_c`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓
- [ ] Expected R²: 0.90-0.97
- [ ] Test Prediction: population=52000, police_per_1000=2.5, unemployment_rate=6.5, avg_income=45000, education_high_school_percent=78, street_lights_working_percent=92, cctv_cameras=45, previous_crimes_30d=18, temperature_c=22
- [ ] Expected Result: ~3.5-4.2 incidents/day

---

## ✅ Dataset 7: Energy Consumption
- [ ] Upload: `7_energy_consumption.csv`
- [ ] Check Analytics: building types and occupancy
- [ ] Target: `energy_consumption_kwh`
- [ ] Features: `floor_area_sqm`, `occupancy_count`, `hvac_efficiency`, `temperature_c`
- [ ] Models: Random Forest ✓, Linear Regression ✓
- [ ] Expected R²: 0.88-0.95
- [ ] Test Prediction: floor_area_sqm=5000, occupancy_count=120, hvac_efficiency=85, temperature_c=22
- [ ] Expected Result: ~3800-3900 kWh

---

## ✅ Dataset 8: Public Transport Demand
- [ ] Upload: `8_public_transport_demand.csv`
- [ ] Check Analytics: peak hour patterns
- [ ] Target: `ridership_count`
- [ ] Features: `hour`, `temperature_c`, `fuel_price`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓
- [ ] Expected R²: 0.75-0.88
- [ ] Test Prediction: hour=8, temperature_c=18, fuel_price=1.45
- [ ] Expected Result: ~440-460 riders

---

## ⚠️ NEW - Dataset 9: Pothole Detection (Road Safety)
- [ ] Upload: `9_pothole_detection.csv`
- [ ] Check Analytics: vibration intensity and depression depth
- [ ] Target: `pothole_severity` (1=minor, 5=severe)
- [ ] Features: `vibration_intensity`, `surface_roughness_mm`, `crack_width_mm`, `depression_depth_mm`, `vehicle_speed_kmh`, `sensor_confidence`, `previous_reports`, `maintenance_age_days`, `traffic_volume`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓, Decision Tree ✓
- [ ] Expected R²: 0.88-0.96
- [ ] Test Prediction: vibration_intensity=5.1, surface_roughness_mm=18.3, crack_width_mm=5.2, depression_depth_mm=65, vehicle_speed_kmh=28.5, sensor_confidence=0.95, previous_reports=5, maintenance_age_days=720, traffic_volume=12000
- [ ] Expected Result: ~5.0 (Level 5 - severe pothole, immediate repair needed)
- [ ] **Purpose:** Prevent accidents by detecting dangerous potholes

---

## ⚠️ NEW - Dataset 10: Road Damage Assessment (Road Safety)
- [ ] Upload: `10_road_damage_assessment.csv`
- [ ] Check Analytics: pavement condition and structural integrity
- [ ] Target: `road_damage_level` (1=excellent, 5=critical)
- [ ] Features: `pavement_condition_index`, `rutting_depth_mm`, `cracking_density_percent`, `surface_distress_area_sqm`, `structural_integrity`, `skid_resistance`, `age_years`, `daily_heavy_vehicles`, `last_maintenance_months`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓
- [ ] Expected R²: 0.90-0.97
- [ ] Test Prediction: pavement_condition_index=32.8, rutting_depth_mm=15.2, cracking_density_percent=38.5, surface_distress_area_sqm=35.2, structural_integrity=48, skid_resistance=42, age_years=18, daily_heavy_vehicles=850, last_maintenance_months=28
- [ ] Expected Result: ~5.0 (Level 5 - critical damage, road closure recommended)
- [ ] **Purpose:** Identify bad roads before they cause accidents

---

## ⚠️ NEW - Dataset 11: Road Diversion Prediction (Traffic Management)
- [ ] Upload: `11_road_diversion_prediction.csv`
- [ ] Check Analytics: traffic density and congestion patterns
- [ ] Target: `diversion_needed` (0=no, 1=yes)
- [ ] Features: `current_traffic_density`, `accident_history_30days`, `road_work_active`, `emergency_vehicles`, `congestion_level`, `avg_travel_time_minutes`, `normal_travel_time_minutes`, `weather_visibility_km`, `road_capacity_used_percent`, `alternative_route_available`
- [ ] Models: Random Forest ✓, Logistic Regression ✓, Gradient Boosting ✓
- [ ] Expected Accuracy: 0.92-0.98
- [ ] Test Prediction (diversion needed): current_traffic_density=92.8, accident_history_30days=4, road_work_active=1, emergency_vehicles=2, congestion_level=4, avg_travel_time_minutes=65, normal_travel_time_minutes=25, weather_visibility_km=3.2, road_capacity_used_percent=98, alternative_route_available=1
- [ ] Expected Result: 1 (YES - diversion needed)
- [ ] **Purpose:** Reduce accidents by proactively diverting traffic from dangerous conditions

---

## ⚠️ NEW - Dataset 12: Work In Progress Zones (Construction Safety)
- [ ] Upload: `12_work_in_progress_zones.csv`
- [ ] Check Analytics: construction activity patterns
- [ ] Target: `work_in_progress` (0=no, 1=yes)
- [ ] Features: `construction_vehicles_count`, `worker_presence`, `machinery_active`, `lane_closure_count`, `safety_barriers_present`, `signage_visibility`, `traffic_control_personnel`, `duration_days`, `heavy_equipment_movement`, `noise_level_db`, `dust_level_pm10`
- [ ] Models: Random Forest ✓, Gradient Boosting ✓, Logistic Regression ✓
- [ ] Expected Accuracy: 0.95-0.99
- [ ] Test Prediction (active work zone): construction_vehicles_count=8, worker_presence=1, machinery_active=1, lane_closure_count=3, safety_barriers_present=1, signage_visibility=2, traffic_control_personnel=3, duration_days=42, heavy_equipment_movement=2, noise_level_db=92, dust_level_pm10=180
- [ ] Expected Result: 1 (YES - work in progress detected)
- [ ] **Purpose:** Alert drivers to construction zones to prevent accidents

---

## 🎯 Overall Progress Tracker

| Dataset | Uploaded | Trained | R²/Acc | Prediction Tested |
|---------|----------|---------|--------|-------------------|
| 1. Flood | ☐ | ☐ | _____ | ☐ |
| 2. AQI | ☐ | ☐ | _____ | ☐ |
| 3. Traffic | ☐ | ☐ | _____ | ☐ |
| 4. Waste | ☐ | ☐ | _____ | ☐ |
| 5. Waterlogging | ☐ | ☐ | _____ | ☐ |
| 6. Crime | ☐ | ☐ | _____ | ☐ |
| 7. Energy | ☐ | ☐ | _____ | ☐ |
| 8. Transport | ☐ | ☐ | _____ | ☐ |
| **9. Pothole (NEW)** | ☐ | ☐ | _____ | ☐ |
| **10. Road Damage (NEW)** | ☐ | ☐ | _____ | ☐ |
| **11. Diversion (NEW)** | ☐ | ☐ | _____ | ☐ |
| **12. Work Zones (NEW)** | ☐ | ☐ | _____ | ☐ |

**Average R² Score:** _____  
**Target:** > 0.85

**🚗 Road Safety Focus:** Datasets 9-12 specifically target accident prevention through early detection of hazardous road conditions!

---

## ⚡ Quick Workflow (Repeat for Each Dataset)

1. **Upload** (30 seconds)
   - Go to Upload page → Drag CSV → Wait for success

2. **Analyze** (1 minute)
   - Go to Analytics → Review statistics → Check for patterns

3. **Visualize** (1 minute)
   - Go to Visualizations → Look at correlation heatmap

4. **Train** (2 minutes)
   - Go to Train Models
   - Select target column
   - Select feature columns (exclude date, ID, category, target)
   - Check 2-3 models
   - Set test size to 20%
   - Click "Train Models"
   - Wait 30-120 seconds

5. **Verify** (30 seconds)
   - Check R² scores
   - Note best performing model

6. **Predict** (1 minute)
   - Go to Predictions
   - Select best model
   - Enter test values
   - Check if prediction makes sense

**Total Time per Dataset:** ~6 minutes  
**Total for All 12 Datasets:** ~72 minutes (1.2 hours)

---

## 🚨 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "No models trained" | Go to Train page first, train before predicting |
| Low R² (<0.60) | Add more features, try Random Forest |
| "Feature not found" | Check exact column names (case-sensitive) |
| Training takes >3 min | Reduce models selected, check backend running |
| Can't find CSV files | Look in `training_datasets/` folder |
| Prediction seems wrong | Check units, verify feature values are realistic |

---

## 📊 R² Score Interpretation

| Score | Quality | Action |
|-------|---------|--------|
| 0.90-1.00 | Excellent | ✅ Ready for production |
| 0.80-0.89 | Good | ✅ Acceptable, consider minor tuning |
| 0.70-0.79 | Fair | ⚠️ Review features, try different model |
| <0.70 | Poor | ❌ Retrain with better features |

---

## 💡 Pro Tips

1. **Always train Random Forest** - usually best performer
2. **Exclude non-numeric columns** - date, location, category shouldn't be features
3. **Check correlations first** - helps select better features
4. **Test extreme values** - validates model makes sense
5. **Document R² scores** - track which datasets perform best
6. **Retrain after changes** - models are session-based only

---

**File Locations:**
- CSV Files: `training_datasets/` folder (8 files)
- Full Guide: `TRAINING_GUIDE.md` (detailed instructions)
- User Guide: `USER_GUIDE.md` (UI walkthrough)

**Happy Training! 🎉**
