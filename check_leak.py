import pandas as pd
import numpy as np

df = pd.read_csv('datasets/waterborne_disease_dataset.csv', nrows=50000)

FEATURE_COLS = [
    'ph', 'turbidity_ntu', 'fecal_coliform_per_100ml', 'total_coliform_per_100ml',
    'tds_mg_l', 'nitrate_mg_l', 'bod_mg_l', 'dissolved_oxygen_mg_l',
    'fluoride_mg_l', 'arsenic_ug_l',
]

print("=== Mean values per disease class ===")
print(df.groupby('disease')[FEATURE_COLS].mean().to_string())

print("\n=== fecal_coliform stats by disease ===")
print(df.groupby('disease')['fecal_coliform_per_100ml'].describe().to_string())

print("\n=== No_Disease rows where fecal_coliform > 0 ===")
no_dis = df[df['disease'] == 'No_Disease']
print(f"fecal_coliform > 0: {(no_dis['fecal_coliform_per_100ml'] > 0).sum()} / {len(no_dis)}")

print("\n=== Disease rows where fecal_coliform == 0 ===")
dis = df[df['disease'] != 'No_Disease']
print(f"fecal_coliform == 0: {(dis['fecal_coliform_per_100ml'] == 0).sum()} / {len(dis)}")

print("\n=== Correlation of each feature with disease label ===")
y = (df['disease'] != 'No_Disease').astype(int)
for col in FEATURE_COLS:
    corr = df[col].corr(y)
    print(f"  {col}: {corr:.4f}")
