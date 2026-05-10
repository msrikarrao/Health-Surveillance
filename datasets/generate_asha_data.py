import json
from datetime import datetime

# ASHA worker collection data - captures front-line worker observations
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

import pandas as pd
df_asha = pd.DataFrame(asha_data)
df_asha.to_csv('asha_worker_data.csv', index=False)
print("✅ ASHA Worker Data:", len(df_asha), "records")
