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

🦌 Overview

Wildlife conservation begins with understanding where animals live, move, and thrive.
Wildlife Sightings Logger & Spatial Mapper is an object-oriented Python application that provides a structured way to record wildlife observations and analyze their geographical relationship with protected conservation areas.
By combining geospatial analysis, persistent JSON storage, and interactive mapping, this project transforms simple field observations into meaningful spatial insights.

✨ Features
Feature	Description
🐾 Wildlife Sightings Logging	Record wildlife observations with species names, geographical coordinates, dates, and other relevant details.
🏞️ Protected Zone Management	Define conservation reserves using multi-vertex geographical polygon boundaries.
📍 Geospatial Boundary Analysis	Use Shapely to determine whether wildlife sightings fall inside or outside protected areas.
💾 Persistent JSON Storage	Automatically serialize and deserialize wildlife records to maintain data across application sessions.
🗺️ Interactive Map Visualization	Generate interactive geographical maps using Folium with wildlife markers and reserve boundaries.
🚨 Species Classification	Distinguish endangered species (🔴 Red) from common species (🔵 Blue) through color-coded map markers.
🧩 Object-Oriented Architecture	Organize functionality into reusable classes: Sighting, ProtectedZone, WildlifeTracker, and MapExporter.
🌍 Conservation Monitoring	Visualize the spatial relationship between wildlife observations and protected conservation zones.

🛠️ Tech Stack
Python – Core application development
Shapely – Geometric operations and spatial boundary analysis
Folium – Interactive geographical visualization
JSON – Lightweight data persistence

📂 Project Structure

wildlife-sightings-mapper/
│
├── data/
│   └── sightings.json          # Persistent wildlife records
│
├── output/
│   └── wildlife_map.html       # Generated interactive map
│
├── src/
│   ├── models.py               # Sighting & ProtectedZone classes
│   ├── tracker.py              # Data management & spatial queries
│   └── mapper.py               # Folium map generation
│
├── main.py                     # Application entry point
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation

🗺️ How It Works

The application follows a modular object-oriented architecture.
Record Sightings: Wildlife observations are captured with species information and geographical coordinates.
Define Protected Areas: Conservation reserves are represented as polygon geometries.
Perform Spatial Analysis: Shapely evaluates the geographical relationship between sightings and protected boundaries.
Store Observations: Records are serialized into JSON for persistence across sessions.
Generate Visualizations: Folium creates interactive maps containing wildlife markers and conservation boundaries.

🎨 Map Legend
Marker	            Meaning
🔴 Red	            Endangered species
🔵 Blue 	          Common species
🟢 Green boundary	  Protected conservation zone

🧠 Object-Oriented Design

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
<i>Built with Python and a passion for biodiversity.</i>
</p>
