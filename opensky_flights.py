import requests
import json
from datetime import datetime

# Step 1: Fetch live flight data from OpenSky API
print("Fetching live aircraft data...")
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Step 2: Prepare GeoJSON format
features = []
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
                "time_position": datetime.utcfromtimestamp(state[3]).isoformat() if state[3] else "N/A",
                "altitude": state[7],
                "velocity": state[9],
                "heading": state[10]
            }
        }
        features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Step 3: Save as .geojson file
filename = "opensky_flights.geojson"
with open(filename, "w") as f:
    json.dump(geojson_data, f, indent=2)

print(f"GeoJSON saved as: {filename}")