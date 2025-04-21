import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

# Step 1: Fetch live aircraft data from OpenSky API
print("Fetching live aircraft data...")
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Step 2: Prepare new features (points) for this batch
new_features = []
now = datetime.utcnow()
cutoff_time = now - timedelta(hours=24)  # 24-hour cutoff

for state in data.get("states", []):
    lon = state[5]
    lat = state[6]
    if lon is not None and lat is not None:
        new_features.append({
            "icao24": state[0],
            "callsign": state[1].strip() if state[1] else "",
            "origin_country": state[2],
            "time_position": state[3],
            "timestamp_iso": datetime.utcfromtimestamp(state[3]).isoformat() if state[3] else now.isoformat(),
            "lon": lon,
            "lat": lat,
            "altitude": state[7],
        })

# Step 3: Load and filter existing data
filename = "flight_points.json"
all_features = []

if os.path.exists(filename):
    with open(filename, "r") as f:
        try:
            # Load existing features and filter by time
            existing_features = json.load(f)
            for feature in existing_features + new_features:
                # Parse timestamp with error handling
                try:
                    feature_time = datetime.fromisoformat(feature.get("timestamp_iso"))
                except (ValueError, TypeError):
                    continue
                
                if feature_time >= cutoff_time:
                    all_features.append(feature)
        except json.JSONDecodeError:
            all_features = new_features
else:
    all_features = new_features

# Step 4: Save filtered data
with open(filename, "w") as f:
    json.dump(all_features, f, indent=2)

# Step 5: Create trajectories (keep only last 24 hours)
df = pd.DataFrame(all_features)
trajectories = []

for icao24, group in df.groupby("icao24"):
    group = group.sort_values("time_position")
    if len(group) > 1:
        coords = list(zip(group["lon"], group["lat"]))
        traj = LineString(coords)
        trajectories.append({"icao24": icao24, "geometry": traj})

# Step 6: Save trajectories (always create valid file)
traj_filename = "flight_trajectories.geojson"
if trajectories:
    gdf = gpd.GeoDataFrame(trajectories, crs="EPSG:4326")
    gdf.to_file(traj_filename, driver="GeoJSON")
    print(f"Trajectories saved as: {traj_filename}")
else:
    # Create empty GeoJSON if no trajectories
    empty_geojson = {"type": "FeatureCollection", "features": []}
    with open(traj_filename, "w") as f:
        json.dump(empty_geojson, f, indent=2)
    print("No trajectories to save yet")

print(f"Total features kept: {len(all_features)} (24-hour window)")
