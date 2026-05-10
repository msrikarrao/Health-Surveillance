import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# IoT Water Quality Sensor Data - real-time water monitoring
iot_water_data = []

# Sensor locations
sensors = [
    {"sensor_id": "IOT_W001", "location": "Village_A_Well", "source_type": "well", "district": "Assam"},
    {"sensor_id": "IOT_W002", "location": "Village_B_Tap", "source_type": "tap", "district": "Assam"},
    {"sensor_id": "IOT_W003", "location": "Village_C_River", "source_type": "river", "district": "Tripura"},
    {"sensor_id": "IOT_W004", "location": "Village_D_Tank", "source_type": "tank", "district": "Meghalaya"},
    {"sensor_id": "IOT_W005", "location": "Village_E_Well", "source_type": "well", "district": "Manipur"},
]

# Normal and contaminated ranges
normal_ranges = {
    "turbidity": {"normal": (0, 5), "contaminated": (5, 50)},  # NTU
    "ph": {"normal": (6.5, 8.5), "contaminated": (4, 10)},     # pH scale
    "bacterial_count": {"normal": (0, 100), "contaminated": (100, 10000)},  # CFU/mL
    "nitrate": {"normal": (0, 10), "contaminated": (10, 100)}, # mg/L
    "chlorine": {"normal": (0.5, 2), "contaminated": (0, 0.5)},  # mg/L
}

# Generate IoT readings (daily measurements over 3 months)
start_date = datetime(2026, 2, 1)
for sensor in sensors:
    for day in range(90):  # 3 months of daily readings
        reading_date = start_date + timedelta(days=day)
        
        # Simulate contamination events (20% chance on river sources)
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
print("✅ IoT Water Quality Data:", len(df_iot), "records")
print("\nContamination Summary by Source Type:")
print(df_iot.groupby('source_type')['contamination_flag'].agg(['sum', 'count', 'mean']))
