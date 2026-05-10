import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Seasonal data - captures disease patterns by season
seasonal_data = []

# Define season characteristics for water-borne diseases
seasons = {
    "monsoon": {"month": [6, 7, 8, 9], "humidity": 85, "rainfall": 450, "disease_risk": 0.8},
    "post_monsoon": {"month": [10, 11], "humidity": 75, "rainfall": 150, "disease_risk": 0.6},
    "winter": {"month": [12, 1, 2], "humidity": 60, "rainfall": 50, "disease_risk": 0.3},
    "summer": {"month": [3, 4, 5], "humidity": 70, "rainfall": 100, "disease_risk": 0.5},
}

# Generate seasonal data for the past 2 years
start_date = datetime(2024, 1, 1)
for i in range(24):  # 24 months
    current_date = start_date + timedelta(days=30*i)
    month = current_date.month
    
    # Determine season
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
df_seasonal.to_csv('seasonal_data.csv', index=False)
print("✅ Seasonal Data:", len(df_seasonal), "records")
print("\nSample:")
print(df_seasonal.head())
