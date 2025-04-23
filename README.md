# Aircraft GIS Visualization Project

## Overview

This project demonstrates the collection, processing, and visualization of global flight position data from the OpenSky Network API. The workflow accumulates 24 hours of aircraft position data, prepares time-enabled GIS layers, and provides clear visualizations using ArcGIS Online — all without requiring a live data feed or paid cloud automation.

## Features

- **24-Hour Rolling Dataset:**  
  The system accumulates and retains only the last 24 hours of aircraft positions, ensuring a manageable file size and showing a full day of flight activity for analysis and animation.

- **Time-Enabled and Trajectory Layers:**  
  - `24h_flight_points.geojson`: Aircraft positions, each with a timestamp, suitable for time slider animation and heat map creation.
  - `24h_flight_trajectories.geojson`: Trajectory lines for each aircraft, representing movement over the past day.

- **Interactive GIS Visualization:**  
  - Upload the GeoJSON files as hosted feature layers in ArcGIS Online.
  - Enable the time slider on the points layer, allowing users to animate and explore movements through the 24-hour window.
  - Style the map to show:
    - **Heatmaps** when zoomed out (for regional/global density)
    - **Points and trajectories** when zoomed in (for detail)
    - **Pop-ups** with flight details for each point when clicked

## Workflow

1. **Data Collection (Automated Script):**
   - Python script collects new aircraft data every 30 minutes and appends it to the cumulative 24-hour dataset.
   - Results are saved as GeoJSON files: `24h_flight_points.geojson` (points) and `24h_flight_trajectories.geojson` (lines).
2. **Manual Demonstration Workflow:**  
   - Download the latest GeoJSON files from the GitHub repository.
   - Upload as hosted feature layers in ArcGIS Online.
   - Enable time on the points layer (using `timestamp_iso`).
   - Configure symbology/visibility for heatmaps and trajectories.

## Example Visualizations

| Heatmap (Zoomed Out)                                  | Points & Trajectories (Zoomed In)          |
|-------------------------------------------------------|--------------------------------------------|
| ![](screenshots/Screenshot%202025-04-21%20at%205.07.29%E2%80%AFPM.png) | ![](screenshots/Screenshot%202025-04-21%20at%205.07.15%E2%80%AFPM.png) |

> [View the interactive time-enabled map on ArcGIS Online](https://www.arcgis.com/home/webmap/viewer.html?webmap=684cb8e26a814139ad05975ef523cbf2)  
> *(If you receive a 403 error, copy and paste this link into a new browser tab.)*

## How to Reproduce or Demonstrate

1. Clone this repository and let the GitHub Actions workflow run for at least 24 hours to accumulate data.
2. Download the `24h_flight_points.geojson` and `24h_flight_trajectories.geojson` files.
3. In ArcGIS Online:
    - Upload as hosted feature layers.
    - Enable time using the `timestamp_iso` field on the points layer.
    - Style layers for heatmap, points, and trajectories, using scale-dependent visibility.
    - Use the time slider for animation.

## Key Skills Demonstrated

- Python scripting, REST API usage, and workflow automation
- Geospatial data processing and time-enabled GIS analysis
- Data visualization with ArcGIS Online (heatmap, time slider, trajectories)
- Professional cartographic design with scale-dependent symbology

## Notes

- **No live feed required:** The demo uses a rolling 24-hour dataset, updated automatically by code and manually uploaded for each demonstration.
- **ArcGIS Online limitation:** Time slider animation is only available on hosted feature layers, which do not auto-update from external URLs (see README for details).
- **For best results:** Update the hosted feature layers with new datasets before each presentation/demo.

## References

- [OpenSky Network API](https://opensky-network.org/apidoc/rest.html)
- [ArcGIS Online Feature Layer Documentation](https://doc.arcgis.com/en/arcgis-online/)
- [GeoJSON Format](https://geojson.org/)

---

*Created for GIS portfolio, analysis, and educational demonstration.*
