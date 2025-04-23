import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

# SETTINGS
WINDOW_HOURS = 12  # Rolling window duration
RUN_INTERVAL_MIN = 30  # Script runs every 30 min

now = datetime.utcnow()
cutoff_time = now - timedelta(hours=WINDOW_HOURS)
points_filename = "flight_points.geojson"
traj_filename = "flight_trajectories.geojson"

# Step 1: Fetch aircraft data
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Step 2: Load and trim existing points
if os.path.exists(points_filename):
    with open(points_filename, "r") as f:
        existing_data = json.load(f)
        all_features = existing_data["features"]
else:
    all_features = []

# Step 3: Only keep points from the last N hours
def feature_time(feature):
    try:
        return datetime.fromisoformat(feature["properties"]["timestamp_iso"])
    except Exception:
        return None
all_features = [f for f in all_features if feature_time(f) and feature_time(f) >= cutoff_time]

# Step 4: Append new points (from current fetch)
for state in data.get("states", []):
    lon, lat = state[5], state[6]
    if lon is not None and lat is not None:
        timestamp_iso = (
            datetime.utcfromtimestamp(state[3]).isoformat()
            if state[3] else now.isoformat()
        )
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "icao24": state[0],
                "callsign": (state[1] or "").strip(),
                "origin_country": state[2],
                "time_position": state[3],
                "timestamp_iso": timestamp_iso,
                "altitude": state[7]
            }
        }
        all_features.append(feature)

# Step 5: Save the last 12 hours of point data
with open(points_filename, "w") as f:
    json.dump({"type": "FeatureCollection", "features": all_features}, f, indent=2)
print(f"Saved {len(all_features)} features to {points_filename}")

# Step 6: Create trajectories for last 12 hours
df = pd.DataFrame([
    {
        "icao24": f["properties"]["icao24"],
        "timestamp_iso": f["properties"]["timestamp_iso"],
        "lon": f["geometry"]["coordinates"][0],
        "lat": f["geometry"]["coordinates"][1]
    }
    for f in all_features
    if f["geometry"]["coordinates"][0] is not None and f["geometry"]["coordinates"][1] is not None
])
trajectories = []
if not df.empty:
    for icao24, group in df.groupby("icao24"):
        group = group.sort_values("timestamp_iso")
        if len(group) > 1:
            coords = list(zip(group["lon"], group["lat"]))
            # Filter out weird verticals (optional)
            coords = [
                (lon, lat) for lon, lat in coords
                if -90 <= lat <= 90 and -180 <= lon <= 180
            ]
            if len(coords) > 1:
                traj = LineString(coords)
                trajectories.append({
                    "type": "Feature",
                    "geometry": traj.__geo_interface__,
                    "properties": {"icao24": icao24}
                })

# Step 7: Save the trajectory lines for the last 12 hours
with open(traj_filename, "w") as f:
    json.dump({"type": "FeatureCollection", "features": trajectories}, f, indent=2)
print(f"Saved {len(trajectories)} trajectories to {traj_filename}")
