# Altitude information for Sri Lanka

## Versions 

* 1.0.1 - Base version

## Data

This library uses **3 arc-second Digital Elevation Models (DEMs)** from the [United States Geological Survey](https://www.usgs.gov/programs/national-geospatial-program/topographic-maps).

### 3 arc-second Digital Elevation Models (DEMs)

3 arc-second Digital Elevation Models (DEMs) are a specific type of elevation data representation used in geographic information systems (GIS) and other applications involving topography and terrain analysis. 

A **Digital Elevation Model (DEM)** is a 3D representation of a terrain's surface created from terrain elevation data. It's a digital model or 3D representation of a terrain's surface — typically of the Earth's surface, but it can be of other planets. DEMs are used in geography, cartography, and surveying, as well as in disciplines like civil engineering, environmental studies, and archaeology.

**3 arc-second** refers to the spatial resolution of the DEM. One arc-second is 1/3600th of a degree of latitude or longitude. Therefore, three arc-seconds means each pixel or grid cell in the DEM represents a square of the Earth's surface that is three arc-seconds by three arc-seconds in size. This roughly translates to about 90 meters by 90 meters at the equator, although the actual ground distance covered by three arc-seconds varies slightly with latitude due to the Earth's curvature.

Thus, an area one latitude by one longitude, is represented by a grid of 1201 by 1201 cells.

## Examples

### [example1_alt_map.py](examples/example1_alt_map.py)

![example1_alt_map.py](examples/example1_alt_map.py.png)

### [example2_slope_map.py](examples/example2_slope_map.py)

![example2_slope_map.py](examples/example2_slope_map.py.png)

### [example3_alt_map_recolored.py](examples/example3_alt_map_recolored.py)

![example3_alt_map_recolored.py](examples/example3_alt_map_recolored.py.png)

*Updated 2024-01-23*