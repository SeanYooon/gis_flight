# Aircraft Movement GIS Visualization (24-Hour Rolling Data)

## Project Overview

This project automates the collection, processing, and visualization of aircraft movement data over a 24-hour rolling period using the OpenSky Network API and Python. The workflow results in two key GeoJSON files for ready demonstration in ArcGIS Online:

- **flight_points.geojson**: A time-enabled point dataset containing all aircraft positions observed over the latest 24 hours, each with a timestamp for temporal animation and heatmap analysis.
- **flight_trajectories.geojson**: Line features representing the 24-hour movement trajectories of each individual aircraft, generated from the accumulated points.

Screenshots of the resulting maps are stored in the **`screenshots`** folder for inclusion in documentation or presentations.

## Data Processing Workflow

1. **Automated Data Updates**
    - The Python script (`opensky_flights.py`) is scheduled via GitHub Actions to run every 30 minutes.
    - Each run:
        - Fetches live aircraft data from OpenSky,
        - Appends new points to `flight_points.geojson`,
        - Removes points older than 24 hours to keep the dataset current and manageable.
        - Updates `flight_trajectories.geojson` to reflect only paths from the last 24 hours.

2. **Manual Visualization Demonstration**
    - After a full 24 hours, download the latest `flight_points.geojson` and `flight_trajectories.geojson` from your repository.
    - Upload `flight_points.geojson` as a hosted feature layer in ArcGIS Online and enable the **time slider** using the `timestamp_iso` field.
    - Upload `flight_trajectories.geojson` for path/line visualization.
    - Style your web map:
        - **Heatmap**: for aircraft density, visible when zoomed out.
        - **Points & Trajectories**: for details, visible when zoomed in.
    - Use the time slider to animate aircraft movement and density across the 24-hour window.

## Example Visualizations

| Heatmap (Zoomed Out)                                  | Points & Trajectories (Zoomed In)          |
|-------------------------------------------------------|--------------------------------------------|
| ![](screenshots/Screenshot%202025-04-21%20at%205.07.29%E2%80%AFPM.png) | ![](screenshots/Screenshot%202025-04-21%20at%205.07.15%E2%80%AFPM.png) |

> [View the interactive time-enabled map on ArcGIS Online](https://www.arcgis.com/home/webmap/viewer.html?webmap=684cb8e26a814139ad05975ef523cbf2)  
> *(If you receive a 403 error, copy and paste this link into a new browser tab.)*

## How to Run the Workflow

- The GitHub Actions workflow (`.github/workflows/update_geojson.yml`) automates running the Python script and updating the GeoJSON files.
- You can also run the script locally:
