🌿 Wildlife Sightings Logger & Spatial Mapper

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9%2B-2E8B57?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Shapely-Geospatial-228B22?style=for-the-badge" />
<img src="https://img.shields.io/badge/Folium-Interactive%20Maps-006400?style=for-the-badge" />
<img src="https://img.shields.io/badge/Storage-JSON-8FBC8F?style=for-the-badge" />
</p>

<p align="center">
<i>Discover. Document. Protect.</i>
<br/>
A Python-based wildlife monitoring system designed to record animal sightings, analyze conservation boundaries, and visualize biodiversity through interactive maps.
</p>


<b>🦌 Overview</b>

Wildlife conservation begins with understanding where animals live, move, and thrive.
Wildlife Sightings Logger & Spatial Mapper is an object-oriented Python application that provides a structured way to record wildlife observations and analyze their geographical relationship with protected conservation areas.
By combining geospatial analysis, persistent JSON storage, and interactive mapping, this project transforms simple field observations into meaningful spatial insights.


<b>✨ Features</b>

| Feature | Description |
|---|---|
| 🐾 Wildlife Logging | Record species, coordinates, dates, and observation details |
| 🖥️ Interactive CLI Menu | Navigate project features through a user-friendly interactive command-line menu with input validation |
| 🏞️ Protected Zones | Define conservation reserves using polygon boundaries |
| 📍 Spatial Analysis | Determine whether sightings fall inside or outside protected areas |
| 💾 Persistent Storage | Automatically save and retrieve sightings using JSON |
| 🗺️ Interactive Maps | Visualize wildlife observations and reserve boundaries |
| 🚨 Species Classification | Distinguish endangered and common species using colored markers |
| 🧩 OOP Architecture | Modular, reusable, and maintainable Python classes |


<b>🛠️ Tech Stack</b>

Python – Core application development

Shapely – Geometric operations and spatial boundary analysis

Folium – Interactive geographical visualization

JSON – Lightweight data persistence


<b>📂 Project Structure</b>

wildlife-sightings-mapper/
│
├── data/
│   └── sightings.json          # Persistent JSON storage for logged sightings
│
├── wildlife_polygon_map.html   # Generated interactive Folium map
│
├── src/
│   ├── __init__.py             # Marks src as a Python package
│   ├── models.py               # Sighting & ProtectedZone (Shapely geometry)
│   ├── tracker.py              # WildlifeTracker (JSON I/O & spatial checks)
│   ├── mapper.py               # MapExporter (Folium HTML rendering)
│   └── cli.py                  # WildlifeCLI (Rich menus, tables & input validation)
│
├── main.py                     # Entry point (tracker, zones, mapper & CLI)
├── requirements.txt            # folium, shapely, rich
├── .gitignore                  # Ignores venv/, __pycache__/, and output/*.html
└── README.md                   # Project documentation


<b>🗺️ How It Works</b>

The application follows a modular object-oriented architecture.
Record Sightings: Wildlife observations are captured with species information and geographical coordinates.
Define Protected Areas: Conservation reserves are represented as polygon geometries.
Perform Spatial Analysis: Shapely evaluates the geographical relationship between sightings and protected boundaries.
Store Observations: Records are serialized into JSON for persistence across sessions.
Generate Visualizations: Folium creates interactive maps containing wildlife markers and conservation boundaries.

<b>🎨 Map Legend</b>


<img width="776" height="221" alt="image" src="https://github.com/user-attachments/assets/8b3b6672-bfb7-439a-8f26-6ea68c3b3a5f" />



<b>🧠 Object-Oriented Design </b>

The application is organized around four primary components:
Sighting: Represents an individual wildlife observation.
ProtectedZone: Defines a geographical conservation boundary.
WildlifeTracker: Handles observation management, JSON persistence, and spatial queries.
MapExporter: Generates interactive maps using Folium.

This separation of responsibilities improves code organization, maintainability, and scalability.



This project is intended for educational and wildlife-conservation purposes.

<p align="center">
🌿 <b>Protect Wildlife. Preserve Nature. Map the Future.</b> 🌿
<br/><br/>
<i>Built with Python and a passion for biodiversity conservation.</i>
</p>
