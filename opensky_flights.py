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
input_filename = "flight_points.geojson"
all_features = []

if os.path.exists(input_filename):
    with open(input_filename, "r") as f:
        existing_data = json.load(f)
        existing_features = existing_data["features"]
        
        # Extract properties from GeoJSON features
        existing_records = [
            {**f["properties"], "lon": f["geometry"]["coordinates"][0], "lat": f["geometry"]["coordinates"][1]}
            for f in existing_features
        ]
else:
    existing_records = []

# Combine existing and new features
combined_features = existing_records + new_features

# Filter by time
all_features = [
    f for f in combined_features
    if datetime.fromisoformat(f["timestamp_iso"]) >= cutoff_time
]

# Step 4: Save as GeoJSON
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [f["lon"], f["lat"]]
            },
            "properties": {k: v for k, v in f.items() if k not in ["lon", "lat"]}
        }
        for f in all_features
    ]
}

with open(input_filename, "w") as f:
    json.dump(geojson_data, f, indent=2)
print(f"Saved {len(all_features)} features to {input_filename}")

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
