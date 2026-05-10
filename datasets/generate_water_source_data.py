import pandas as pd
import numpy as np

# Water Source Infrastructure Data
water_source_data = [
    # Village A - Assam
    {"village": "Village_A", "district": "Assam", "source_type": "well", "count": 3, "age_years": 5, "maintenance_status": "good", "chlorination": 1, "outbreak_history": 1, "infection_rate": 0.15},
    {"village": "Village_A", "district": "Assam", "source_type": "tap", "count": 1, "age_years": 2, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.05},
    
    # Village B - Assam
    {"village": "Village_B", "district": "Assam", "source_type": "river", "count": 2, "age_years": 0, "maintenance_status": "poor", "chlorination": 0, "outbreak_history": 0, "infection_rate": 0.35},
    {"village": "Village_B", "district": "Assam", "source_type": "well", "count": 2, "age_years": 8, "maintenance_status": "fair", "chlorination": 0, "outbreak_history": 0, "infection_rate": 0.20},
    
    # Village C - Tripura
    {"village": "Village_C", "district": "Tripura", "source_type": "tank", "count": 1, "age_years": 10, "maintenance_status": "poor", "chlorination": 0, "outbreak_history": 2, "infection_rate": 0.45},
    {"village": "Village_C", "district": "Tripura", "source_type": "well", "count": 4, "age_years": 6, "maintenance_status": "fair", "chlorination": 0, "outbreak_history": 1, "infection_rate": 0.25},
    
    # Village D - Meghalaya
    {"village": "Village_D", "district": "Meghalaya", "source_type": "well", "count": 2, "age_years": 3, "maintenance_status": "good", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.10},
    {"village": "Village_D", "district": "Meghalaya", "source_type": "tap", "count": 2, "age_years": 1, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.02},
    
    # Village E - Manipur
    {"village": "Village_E", "district": "Manipur", "source_type": "well", "count": 3, "age_years": 2, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.05},
    {"village": "Village_E", "district": "Manipur", "source_type": "tap", "count": 2, "age_years": 1, "maintenance_status": "excellent", "chlorination": 1, "outbreak_history": 0, "infection_rate": 0.02},
]

df_water_source = pd.DataFrame(water_source_data)

# Add risk score based on source type and maintenance
source_risk_scores = {"river": 0.8, "tank": 0.6, "well": 0.4, "tap": 0.1}
maintenance_scores = {"poor": 0.7, "fair": 0.5, "good": 0.3, "excellent": 0.1}

df_water_source['source_risk_score'] = df_water_source['source_type'].map(source_risk_scores)
df_water_source['maintenance_risk_score'] = df_water_source['maintenance_status'].map(maintenance_scores)
df_water_source['total_risk_score'] = (df_water_source['source_risk_score'] + df_water_source['maintenance_risk_score']) / 2
df_water_source['chlorination_protection'] = 1 - (df_water_source['chlorination'] * 0.3)  # Chlorination reduces risk by 30%

df_water_source.to_csv('water_source_data.csv', index=False)
print("✅ Water Source Data:", len(df_water_source), "records")
print("\nSample:")
print(df_water_source[['village', 'source_type', 'maintenance_status', 'total_risk_score', 'infection_rate']].head(10))
