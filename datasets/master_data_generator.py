#!/usr/bin/env python3
"""
Master Data Generator for Health Surveillance System
Generates all required datasets for ML model training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys

print("=" * 70)
print("🚀 MASTER DATA GENERATOR - Smart Health Surveillance System")
print("=" * 70)

# ============================================================================
# 1. ASHA WORKER DATA
# ============================================================================
print("\n📊 Generating ASHA Worker Data...")

asha_data = [
    {"asha_id": "ASHA001", "district": "Assam", "village": "Village_A", "date": "2026-03-01", "reports_count": 15, "vaccination_coverage": 0.75, "awareness_level": "high", "previous_outbreaks": 1},
    {"asha_id": "ASHA002", "district": "Assam", "village": "Village_B", "date": "2026-03-05", "reports_count": 8, "vaccination_coverage": 0.45, "awareness_level": "medium", "previous_outbreaks": 0},
    {"asha_id": "ASHA003", "district": "Tripura", "village": "Village_C", "date": "2026-03-10", "reports_count": 22, "vaccination_coverage": 0.30, "awareness_level": "low", "previous_outbreaks": 2},
    {"asha_id": "ASHA001", "district": "Assam", "village": "Village_A", "date": "2026-03-15", "reports_count": 18, "vaccination_coverage": 0.75, "awareness_level": "high", "previous_outbreaks": 1},
    {"asha_id": "ASHA004", "district": "Meghalaya", "village": "Village_D", "date": "2026-03-20", "reports_count": 12, "vaccination_coverage": 0.60, "awareness_level": "medium", "previous_outbreaks": 0},
    {"asha_id": "ASHA002", "district": "Assam", "village": "Village_B", "date": "2026-03-25", "reports_count": 10, "vaccination_coverage": 0.45, "awareness_level": "medium", "previous_outbreaks": 0},
    {"asha_id": "ASHA003", "district": "Tripura", "village": "Village_C", "date": "2026-04-01", "reports_count": 28, "vaccination_coverage": 0.30, "awareness_level": "low", "previous_outbreaks": 2},
    {"asha_id": "ASHA005", "district": "Manipur", "village": "Village_E", "date": "2026-04-05", "reports_count": 5, "vaccination_coverage": 0.85, "awareness_level": "high", "previous_outbreaks": 0},
]

df_asha = pd.DataFrame(asha_data)
df_asha['awareness_numeric'] = df_asha['awareness_level'].map({'high': 3, 'medium': 2, 'low': 1})
df_asha.to_csv('asha_worker_data.csv', index=False)
print(f"✅ Created: asha_worker_data.csv ({len(df_asha)} records)")

# ============================================================================
# 2. SEASONAL DATA
# ============================================================================
print("\n📊 Generating Seasonal Data...")

seasonal_data = []
seasons = {
    "monsoon": {"month": [6, 7, 8, 9], "humidity": 85, "rainfall": 450, "disease_risk": 0.8},
    "post_monsoon": {"month": [10, 11], "humidity": 75, "rainfall": 150, "disease_risk": 0.6},
    "winter": {"month": [12, 1, 2], "humidity": 60, "rainfall": 50, "disease_risk": 0.3},
    "summer": {"month": [3, 4, 5], "humidity": 70, "rainfall": 100, "disease_risk": 0.5},
}

start_date = datetime(2024, 1, 1)
for i in range(24):  # 24 months
    current_date = start_date + timedelta(days=30*i)
    month = current_date.month
    
    season = None
    for s_name, s_info in seasons.items():
        if month in s_info["month"]:
            season = s_name
            season_info = s_info
            break
    
    seasonal_data.append({
        "date": current_date.strftime("%Y-%m-%d"),
        "month": month,
        "season": season,
        "average_humidity": season_info["humidity"],
        "average_rainfall_mm": season_info["rainfall"],
        "temperature_celsius": np.random.uniform(20, 35),
        "disease_risk_factor": season_info["disease_risk"],
        "historical_outbreak_cases": int(np.random.poisson(season_info["disease_risk"] * 20)),
    })

df_seasonal = pd.DataFrame(seasonal_data)
df_seasonal['season_numeric'] = df_seasonal['season'].map({'monsoon': 3, 'post_monsoon': 2, 'winter': 1, 'summer': 2})
df_seasonal.to_csv('seasonal_data.csv', index=False)
print(f"✅ Created: seasonal_data.csv ({len(df_seasonal)} records)")

# ============================================================================
# 3. IOT WATER QUALITY DATA
# ============================================================================
print("\n📊 Generating IoT Water Quality Data...")

iot_water_data = []
sensors = [
    {"sensor_id": "IOT_W001", "location": "Village_A_Well", "source_type": "well", "district": "Assam"},
    {"sensor_id": "IOT_W002", "location": "Village_B_Tap", "source_type": "tap", "district": "Assam"},
    {"sensor_id": "IOT_W003", "location": "Village_C_River", "source_type": "river", "district": "Tripura"},
    {"sensor_id": "IOT_W004", "location": "Village_D_Tank", "source_type": "tank", "district": "Meghalaya"},
    {"sensor_id": "IOT_W005", "location": "Village_E_Well", "source_type": "well", "district": "Manipur"},
]

normal_ranges = {
    "turbidity": {"normal": (0, 5), "contaminated": (5, 50)},
    "ph": {"normal": (6.5, 8.5), "contaminated": (4, 10)},
    "bacterial_count": {"normal": (0, 100), "contaminated": (100, 10000)},
    "nitrate": {"normal": (0, 10), "contaminated": (10, 100)},
    "chlorine": {"normal": (0.5, 2), "contaminated": (0, 0.5)},
}

start_date = datetime(2026, 2, 1)
for sensor in sensors:
    for day in range(90):
        reading_date = start_date + timedelta(days=day)
        contamination_prob = 0.3 if sensor["source_type"] == "river" else 0.1
        is_contaminated = np.random.random() < contamination_prob
        
        if is_contaminated:
            ranges = {k: v["contaminated"] for k, v in normal_ranges.items()}
        else:
            ranges = {k: v["normal"] for k, v in normal_ranges.items()}
        
        iot_water_data.append({
            "sensor_id": sensor["sensor_id"],
            "location": sensor["location"],
            "source_type": sensor["source_type"],
            "district": sensor["district"],
            "date": reading_date.strftime("%Y-%m-%d"),
            "time": f"{np.random.randint(8, 18):02d}:{np.random.randint(0, 60):02d}",
            "turbidity_ntu": np.random.uniform(ranges["turbidity"][0], ranges["turbidity"][1]),
            "ph": np.random.uniform(ranges["ph"][0], ranges["ph"][1]),
            "bacterial_count_cfu_ml": int(np.random.uniform(ranges["bacterial_count"][0], ranges["bacterial_count"][1])),
            "nitrate_mg_l": np.random.uniform(ranges["nitrate"][0], ranges["nitrate"][1]),
            "chlorine_mg_l": np.random.uniform(ranges["chlorine"][0], ranges["chlorine"][1]),
            "temperature_celsius": np.random.uniform(20, 30),
            "contamination_flag": 1 if is_contaminated else 0,
        })

df_iot = pd.DataFrame(iot_water_data)
df_iot.to_csv('iot_water_quality.csv', index=False)
print(f"✅ Created: iot_water_quality.csv ({len(df_iot)} records)")

# ============================================================================
# 4. WATER SOURCE DATA
# ============================================================================
print("\n📊 Generating Water Source Infrastructure Data...")

water_source_data = [
    {"village": "Village_A", "district": "Assam", "source_type": "well", "count": 3, "age_years": 5, "maintenance_status": "good", "chlorination": 1, "outbreak_history": 1, "infection_rate": 0.15},
    {"village": "Village_A", "district": "Assam", "source_type": "tap", "count": 1, "age_years": 2, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.05},
    {"village": "Village_B", "district": "Assam", "source_type": "river", "count": 2, "age_years": 0, "maintenance_status": "poor", "chlorination": 0, "outbreak_history": 0, "infection_rate": 0.35},
    {"village": "Village_B", "district": "Assam", "source_type": "well", "count": 2, "age_years": 8, "maintenance_status": "fair", "chlorination": 0, "outbreak_history": 0, "infection_rate": 0.20},
    {"village": "Village_C", "district": "Tripura", "source_type": "tank", "count": 1, "age_years": 10, "maintenance_status": "poor", "chlorination": 0, "outbreak_history": 2, "infection_rate": 0.45},
    {"village": "Village_C", "district": "Tripura", "source_type": "well", "count": 4, "age_years": 6, "maintenance_status": "fair", "chlorination": 0, "outbreak_history": 1, "infection_rate": 0.25},
    {"village": "Village_D", "district": "Meghalaya", "source_type": "well", "count": 2, "age_years": 3, "maintenance_status": "good", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.10},
    {"village": "Village_D", "district": "Meghalaya", "source_type": "tap", "count": 2, "age_years": 1, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.02},
    {"village": "Village_E", "district": "Manipur", "source_type": "well", "count": 3, "age_years": 2, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.05},
    {"village": "Village_E", "district": "Manipur", "source_type": "tap", "count": 2, "age_years": 1, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.02},
]

df_water_source = pd.DataFrame(water_source_data)
source_risk_scores = {"river": 0.8, "tank": 0.6, "well": 0.4, "tap": 0.1}
maintenance_scores = {"poor": 0.7, "fair": 0.5, "good": 0.3, "excellent": 0.1}
df_water_source['source_risk_score'] = df_water_source['source_type'].map(source_risk_scores)
df_water_source['maintenance_risk_score'] = df_water_source['maintenance_status'].map(maintenance_scores)
df_water_source['total_risk_score'] = (df_water_source['source_risk_score'] + df_water_source['maintenance_risk_score']) / 2
df_water_source['chlorination_protection'] = 1 - (df_water_source['chlorination'] * 0.3)
df_water_source['source_type_numeric'] = df_water_source['source_type'].map({'tap': 0, 'well': 1, 'tank': 2, 'river': 3})
df_water_source.to_csv('water_source_data.csv', index=False)
print(f"✅ Created: water_source_data.csv ({len(df_water_source)} records)")

# ============================================================================
# 5. SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 70)
print("📋 DATA GENERATION SUMMARY")
print("=" * 70)
print(f"✅ ASHA Worker Data:        {len(df_asha)} records")
print(f"✅ Seasonal Data:           {len(df_seasonal)} records")
print(f"✅ IoT Water Quality Data:  {len(df_iot)} records")
print(f"✅ Water Source Data:       {len(df_water_source)} records")
print(f"✅ Total Records Generated: {len(df_asha) + len(df_seasonal) + len(df_iot) + len(df_water_source)}")
print("\n" + "=" * 70)
print("🎯 All Data Files Created Successfully!")
print("=" * 70)
print("\n📂 Files Created:")
print("   1. asha_worker_data.csv")
print("   2. seasonal_data.csv")
print("   3. iot_water_quality.csv")
print("   4. water_source_data.csv")
print("\n💾 Location: datasets/ directory")
print("\n✅ Ready for ML model training!")
print("=" * 70)
