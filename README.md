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

