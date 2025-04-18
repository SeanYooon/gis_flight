# 1. 누적 저장 (append) 예시
import requests, json, os
from datetime import datetime

url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# 새 데이터 준비
new_features = []
now = datetime.utcnow().isoformat()
for state in data.get("states", []):
    lon, lat = state[5], state[6]
    if lon and lat:
        new_features.append({
            "icao24": state[0],
            "callsign": state[1] or "",
            "origin_country": state[2],
            "time_position": state[3],
            "timestamp_iso": datetime.utcfromtimestamp(state[3]).isoformat() if state[3] else now,
            "lon": lon,
            "lat": lat,
            "altitude": state[7],
        })

# 기존 파일 불러오기
filename = "flight_points.json"
if os.path.exists(filename):
    with open(filename) as f:
        features = json.load(f)
else:
    features = []

# 누적 저장
features.extend(new_features)
with open(filename, "w") as f:
    json.dump(features, f, indent=2)

# 2. Trajectory(경로) 생성 (pandas, geopandas, shapely 필요)
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

df = pd.DataFrame(features)
trajectories = []
for icao24, group in df.groupby("icao24"):
    group = group.sort_values("time_position")
    if len(group) > 1:
        coords = list(zip(group["lon"], group["lat"]))
        traj = LineString(coords)
        trajectories.append({"icao24": icao24, "geometry": traj})

gdf = gpd.GeoDataFrame(trajectories, crs="EPSG:4326")
gdf.to_file("flight_trajectories.geojson", driver="GeoJSON")

