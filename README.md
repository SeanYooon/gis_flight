# Live Aircraft GIS Visualization Project

## Overview

This project automates the collection, processing, and visualization of live aircraft position data using the OpenSky Network API. Data is automatically fetched every 30 minutes, converted to time-enabled GeoJSON, and visualized in ArcGIS Online to showcase both real-time and historical flight movement patterns.

## Features

- **Automated Real-Time Data Collection:** Uses Python and GitHub Actions to fetch global aircraft position data every 30 minutes.
- **Data Transformation:** Cleans and converts API data to GeoJSON, retaining only the past 24 hours to manage file size and relevance.
- **GIS-Ready Outputs:** Produces two GeoJSON files:
  - `flight_points.geojson`: All flight points in the last 24 hours (time-enabled for animation).
  - `flight_trajectories.geojson`: Trajectory lines for each aircraft’s movement in the last 24 hours.
- **Interactive Web Mapping:** Data is published and visualized in ArcGIS Online featuring:
  - **Point layers** with pop-up info (callsign, country, altitude, etc.)
  - **Heat maps** of flight density (hotspots)
  - **Flight trajectories** as interactive line layers
  - **Time slider** for animated temporal exploration

## How It Works

1. **Data Fetching:** The Python script connects to the OpenSky Network API to gather state vectors (positions) for all visible aircraft.
2. **Data Processing:** Each run filters and keeps only the last 24 hours of data to ensure manageable file sizes.
3. **GeoJSON Export:** Both point and trajectory data are exported in GeoJSON format.
4. **Automation:** GitHub Actions runs the script, updates the files, and pushes them to the repository automatically.
5. **Web Mapping:** The resulting `flight_points.geojson` can be published as a hosted feature layer in ArcGIS Online for full time-enabled visualization with a timeline slider!

## Usage

### Local

1. Clone this repository.
2. Install dependencies:


## Cartographic Design: Scale-Dependent Visualization

To maximize both overview and detail, this project applies **scale-dependent layer visibility** (visibility ranges) in ArcGIS Online:

- **Heat Map:**  
  - Displays only at small scales (when zoomed out, e.g., country or continent level) to reveal broad flight density patterns.
- **Points and Trajectories:**  
  - Become visible at larger scales (when zoomed in to region/city/airport level), showing individual aircraft locations and their paths with high granularity.

**How It Works in the Web Map:**
- When first opened or viewed at a regional or global extent, only the heatmap is visible, making it easy to spot areas of high air traffic.
- As the user zooms in, the map automatically reveals the exact aircraft points and their trajectories, providing detailed, interactive information about specific flights.

**Implementation:**  
This is achieved in ArcGIS Online by setting each layer’s “Set visibility range” property—ensuring optimal performance and a clear, uncluttered map at every zoom level.

> _This design mimics professional air traffic analysis dashboards: patterns at a glance, details on demand._

---

## Example Cartographic Workflow

1. **Upload all data layers** (heat map, points, trajectories) to your ArcGIS Online web map.
2. For each layer, use the three dots (**...**) > **Set visibility range**.
   - **Heat map:** set a minimum scale (e.g., only visible at 1:3,000,000 and smaller).
   - **Points and trajectories:** set a maximum scale (e.g., only visible at 1:1,000,000 and larger).
3. Preview your map, and adjust visibility ranges for desired effect and clarity.

---

[View the interactive time-enabled map on ArcGIS Online](https://simonfraseru.maps.arcgis.com/apps/mapviewer/index.html?webmap=684cb8e26a814139ad05975ef523cbf2)
