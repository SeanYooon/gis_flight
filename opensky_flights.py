import requests
import json
from datetime import datetime
import os

# Step 1: Fetch live flight data from OpenSky API
print("Fetching live aircraft data...")
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Step 2: Prepare GeoJSON features for this batch
new_features = []
for state in data.get("states", []):
    lon = state[5]
    lat = state[6]
    if lon is not None and lat is not None:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "icao24": state[0],
                "callsign": state[1].strip() if state[1] else "N/A",
                "origin_country": state[2],
                "time_position": datetime.utcfromtimestamp(state[3]).isoformat() if state[3] else datetime.utcnow().isoformat(),
                "altitude": state[7],
                "velocity": state[9],
                "heading": state[10]
            }
        }
        new_features.append(feature)

# Step 3: Load previous data if exists, else start new
filename = "opensky_flights.geojson"
if os.path.exists(filename):
    with open(filename, "r") as f:
        try:
            geojson_data = json.load(f)
            features = geojson_data.get("features", [])
        except Exception:
            features = []
else:
    features = []

# Step 4: Append new features
features.extend(new_features)

# Step 5: Save as .geojson file
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

with open(filename, "w") as f:
    json.dump(geojson_data, f, indent=2)

print(f"GeoJSON saved as: {filename} (appended {len(new_features)} new features)")
