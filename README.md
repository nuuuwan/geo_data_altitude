# Altitude information for Sri Lanka

## Versions

### 1.1.x

* Added 1-arc-second DEM data.

### 1.0.x

* Base Version

## Data

This library uses **1 arc-second Digital Elevation Models (DEMs)** from the [United States Geological Survey](https://earthexplorer.usgs.gov/).

![https://earthexplorer.usgs.gov/](readme-1.png)

### Digital Elevation Model (DEM) 

DEM is a 3D representation of a terrain's surface created from terrain elevation data. It's a digital model or 3D representation of a terrain's surface — typically of the Earth's surface, but it can be of other planets. DEMs are used in geography, cartography, and surveying, as well as in disciplines like civil engineering, environmental studies, and archaeology.

### 1 arc-second

This refers to the spatial resolution of the DEM. One arc-second is 1/3600th of a degree of latitude or longitude. Therefore, a one arc-second resolution means each pixel or grid cell in the DEM represents a square of the Earth's surface that is one arc-second by one arc-second in size. This roughly translates to about 30 meters by 30 meters at the equator, although the actual ground distance covered by one arc-second varies slightly with latitude due to the Earth's curvature. Thus, an area one latitude by one longitude, is represented by a grid of 3601 by 3601 cells.

## Examples

### [example1_alt_map.py](examples/example1_alt_map.py)

![example1_alt_map.py](examples/example1_alt_map.py.png)

### [example2_slope_map.py](examples/example2_slope_map.py)

![example2_slope_map.py](examples/example2_slope_map.py.png)

### [example3_alt_map_recolored.py](examples/example3_alt_map_recolored.py)

![example3_alt_map_recolored.py](examples/example3_alt_map_recolored.py.png)

