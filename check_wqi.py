import pandas as pd
import numpy as np

df = pd.read_csv('datasets/waterborne_disease_dataset.csv', nrows=50000)

FEATURE_COLS = ['ph', 'turbidity_ntu', 'tds_mg_l', 'nitrate_mg_l',
                'bod_mg_l', 'dissolved_oxygen_mg_l', 'fluoride_mg_l', 'arsenic_ug_l']

y = (df['water_quality_index'] >= 50).astype(int)
print(f"Class balance — Safe: {(y==1).sum()}, Contaminated: {(y==0).sum()}")
print("\n=== Correlation with WQI>=50 label ===")
for col in FEATURE_COLS:
    print(f"  {col}: {df[col].corr(y):.4f}")

print("\n=== Mean per class ===")
df['label'] = y
print(df.groupby('label')[FEATURE_COLS].mean().to_string())

print("\n=== WQI formula check — correlation of WQI with each feature ===")
for col in FEATURE_COLS:
    print(f"  {col} vs water_quality_index: {df[col].corr(df['water_quality_index']):.4f}")
