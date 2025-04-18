import requests
import json
import os
from datetime import datetime
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
now = datetime.utcnow().isoformat()
for state in data.get("states", []):
    lon = state[5]
    lat = state[6]
    if lon is not None and lat is not None:
        new_features.append({
            "icao24": state[0],  # Unique aircraft identifier
            "callsign": state[1].strip() if state[1] else "",  # Aircraft callsign
            "origin_country": state[2],  # Country of origin
            "time_position": state[3],  # Timestamp (UNIX)
            "timestamp_iso": datetime.utcfromtimestamp(state[3]).isoformat() if state[3] else now,  # ISO timestamp
            "lon": lon,  # Longitude
            "lat": lat,  # Latitude
            "altitude": state[7],  # Altitude
        })

# Step 3: Load previous data if exists, else start new
filename = "flight_points.json"
if os.path.exists(filename):
    with open(filename) as f:
        features = json.load(f)
else:
    features = []

# Step 4: Append new features to the existing data
features.extend(new_features)
with open(filename, "w") as f:
    json.dump(features, f, indent=2)

# Step 5: Create trajectories (lines) for each aircraft
# Load the accumulated point data into a DataFrame
df = pd.DataFrame(features)
trajectories = []
for icao24, group in df.groupby("icao24"):
    group = group.sort_values("time_position")  # Sort by time
    if len(group) > 1:  # Only create a line if there are at least 2 points
        coords = list(zip(group["lon"], group["lat"]))
        traj = LineString(coords)
        trajectories.append({"icao24": icao24, "geometry": traj})

# Step 6: Save the trajectories as a GeoJSON file
if trajectories:
    gdf = gpd.GeoDataFrame(trajectories, crs="EPSG:4326")
    gdf.to_file("flight_trajectories.geojson", driver="GeoJSON")
    print("Trajectories saved as: flight_trajectories.geojson")
else:
    print("No trajectories to save (not enough data yet)")

print(f"Appended {len(new_features)} new features. Total features: {len(features)}")
