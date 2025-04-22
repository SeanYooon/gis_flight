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

now = datetime.utcnow()
cutoff_time = now - timedelta(hours=24)
points_filename = "flight_points.geojson"

# Step 2: Load existing points for accumulation
if os.path.exists(points_filename):
    with open(points_filename, "r") as f:
        existing_data = json.load(f)
        existing_features = existing_data.get("features", [])
else:
    existing_features = []

# Step 3: Filter existing points to only those within the last 24 hours
recent_features = []
for feature in existing_features:
    timestamp = feature["properties"].get("timestamp_iso")
    try:
        ft = datetime.fromisoformat(timestamp)
        if ft >= cutoff_time:
            recent_features.append(feature)
    except Exception:
        continue

# Step 4: Add new points from current API call
for state in data.get("states", []):
    lon = state[5]
    lat = state[6]
    if lon is not None and lat is not None:
        time_position = state[3]
        timestamp_iso = datetime.utcfromtimestamp(time_position).isoformat() if time_position else now.isoformat()
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "icao24": state[0],
                "callsign": state[1].strip() if state[1] else "",
                "origin_country": state[2],
                "time_position": time_position,
                "timestamp_iso": timestamp_iso,
                "lon": lon,
                "lat": lat,
                "altitude": state[7]
            }
        }
        recent_features.append(feature)

# Step 5: Save all accumulated points for 24 hours as GeoJSON
geojson_points = {
    "type": "FeatureCollection",
    "features": recent_features
}
with open(points_filename, "w") as f:
    json.dump(geojson_points, f, indent=2)
print(f"Saved {len(recent_features)} features to {points_filename}")

# Step 6: Create trajectory lines for each aircraft in the last 24 hours
# Convert features into a DataFrame for grouping
df = pd.DataFrame([
    {
        **f["properties"],
        "lon": f["geometry"]["coordinates"][0],
        "lat": f["geometry"]["coordinates"][1]
    }
    for f in recent_features
])
trajectories = []
if not df.empty:
    for icao24, group in df.groupby("icao24"):
        group = group.sort_values("time_position")
        if len(group) > 1:
            coords = list(zip(group["lon"], group["lat"]))
            traj = LineString(coords)
            trajectories.append({"icao24": icao24, "geometry": traj})

# Step 7: Save trajectories (always create a valid GeoJSON file)
traj_filename = "flight_trajectories.geojson"
if trajectories:
    gdf = gpd.GeoDataFrame(trajectories, crs="EPSG:4326")
    gdf.to_file(traj_filename, driver="GeoJSON")
    print(f"Trajectories saved as: {traj_filename}")
else:
    empty_geojson = {"type": "FeatureCollection", "features": []}
    with open(traj_filename, "w") as f:
        json.dump(empty_geojson, f, indent=2)
    print("No trajectories to save yet.")

print("Script completed successfully.")
