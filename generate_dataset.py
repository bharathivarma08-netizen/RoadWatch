import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 1000

data = {
    "crack_area_px":    np.random.randint(50, 5000, n),
    "depth_estimate":   np.round(np.random.uniform(0.5, 15.0, n), 2),
    "pothole_width_px": np.random.randint(20, 800, n),
    "brightness_diff":  np.random.randint(10, 200, n),
    "road_type":        np.random.choice([0, 1, 2], n),  # 0=highway, 1=city, 2=lane
}

df = pd.DataFrame(data)

def label(row):
    score = 0
    if row["crack_area_px"] > 3000:   score += 2
    elif row["crack_area_px"] > 1500: score += 1
    if row["depth_estimate"] > 10:    score += 2
    elif row["depth_estimate"] > 5:   score += 1
    if row["pothole_width_px"] > 500: score += 2
    elif row["pothole_width_px"] > 200: score += 1
    if score >= 4: return "High"
    elif score >= 2: return "Medium"
    else: return "Low"

df["severity"] = df.apply(label, axis=1)
os.makedirs("data", exist_ok=True)
df.to_csv("data/pothole_data.csv", index=False)
print(df["severity"].value_counts())
print("Dataset saved to data/pothole_data.csv")