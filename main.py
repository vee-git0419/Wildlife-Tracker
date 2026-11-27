from datetime import datetime
import json 
from shapely.geometry import Point, Polygon
from shapely.geometry import mapping
import folium 

from src.models import ProtectedZone
from src.tracker import WildlifeTracker
from src.mapper import MapExporter
from src.cli import WildlifeCli

class Sighting:
    #store facts of an observation
    def __init__(self, species: str, lat: float, lon: float, count: int = 1, is_endangered: bool = False, timestamp: str | None = None):
        #Normalization: Clean and format the species string consistently
        self.species = species.strip().title()
        #Type Casting: Ensure correct data types to prevent serialization
        self.lat = float(lat)
        self.lon = float(lon)
        self.count = int(count)
        self.is_endangered = bool(is_endangered)
        #Automatically generate and format a readable date and time for when an observation is recorded.
        #JSON files cannot directly save Python datetime objects. String formatting allows you to easily save, read, and serialize your wildlife data without formatting errors.
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Check if latitude and longitude fall within valid global ranges
        if not (-90 <= self.lat <= 90):
            raise ValueError(f"Invalid latitude: {self.lat}. Must be between -90 and 90.")
        if not (-180 <= self.lon <= 180):
            raise ValueError(f"Invalid longitude: {self.lon}. Must be between -180 and 180.")

    #Bridges the gap between your custom object and Python's json module by packing all object attributes into a clean dictionary.
    def to_dict(self) -> dict:
        """Converts the Sighting object into a standard dictionary for JSON storage."""
        return {
            "species": self.species,
            "lat": self.lat,
            "lon": self.lon,
            "count": self.count,
            "is_endangered": self.is_endangered,
            "timestamp": self.timestamp
        }
    #Factory method used when reconstructing objects from external storage like JSON or CSV files
    @classmethod
    def from_dict(cls, data: dict) -> "Sighting":
        """Recreates a Sighting object from a dictionary loaded from JSON."""
        return cls(
            species=data["species"],
            lat=data["lat"],
            lon=data["lon"],
            count=data["count"],
            is_endangered=data["is_endangered"],
            timestamp=data.get("timestamp") #Keeps the original saved timestamp!
        )
    def __str__(self) -> str:
        """Returns a human-readable string representation of the sighting."""
        status = "[ENDANGERED]" if self.is_endangered else "[COMMON]"
        return f"{status} {self.count}x {self.species} @ ({self.lat}, {self.lon}) - {self.timestamp}"


class ProtectedZone:
    """Represents a conservation park/sanctuary using Shapely vector Polygons."""
    def __init__(self, name: str, coordinates: list[tuple[float, float]]):
        self.name = name
        # Shapely expects coordinates as (longitude, latitude) -> (x, y)
        self.polygon = Polygon(coordinates)

        # Detects self-intersecting or "bowtie" polygons
        if not self.polygon.is_valid:
            raise ValueError(f"Invalid polygon boundary for zone: {name}")
        

    def contains(self, lat: float, lon: float) -> bool:
        point = Point(lon, lat)
        return self.polygon.contains(point) or self.polygon.touches(point)

    #Bridging Shapely to Folium via to_geojson()
    def to_geojson(self) -> dict:
        """Returns a standard GeoJSON feature dictionary."""
        return {
             "type": "Feature",
             "properties": {"name": self.name},
             "geometry": mapping(self.polygon)
       }

#Data manager and storage
class WildlifeTracker:
    def __init__(self, filepath: str = "sightings.json"):
        #Store the filepath with a flexible default
        self.filepath = filepath
        #Initialize an empty list to hold active sightings in memory
        self.sightings: list[Sighting] = []
        self.zones: list[ProtectedZone] = []
        #Boot-up Sequence: Automatically load past records upon instantiation
        self.load_data()
        

    def log_sighting(self, sighting: Sighting):
        """Appends a new sighting and immediately auto-saves to maintain persistence."""
        self.sightings.append(sighting)
        self.save_data()

        # Spatial check using list comprehension across all zones
        in_zones = [z.name for z in self.zones if z.contains(sighting.lat, sighting.lon)]
        zone_info = f"Inside: {', '.join(in_zones)}" if in_zones else "Outside protected zones"
        print(f"[LOGGED] {sighting.count} x {sighting.species} ({zone_info})")


    def save_data(self):
        """Serializes the list of sighting objects to a JSON file."""
        data_to_save = [s.to_dict() for s in self.sightings]
        with open(self.filepath, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def load_data(self):
        """Loads sightings from the JSON file (if available) back into standard python data structures."""
        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
                self.sightings = [Sighting.from_dict(item) for item in raw_data]
        except FileNotFoundError:
            self.sightings = []

    def add_zone(self, zone: ProtectedZone):
        self.zones.append(zone)

    def export_interactive_map(self, output_file: str = "map.html"):
        """Generates an HTML map rendering both vector boundaries and sighting markers."""
        # Guard against an empty sightings list
        if not self.sightings:
            print("No sightings available to map.")
            return

        # Compute average latitude and longitude to center the base map
        avg_lat = sum(s.lat for s in self.sightings) / len(self.sightings)
        avg_lon = sum(s.lon for s in self.sightings) / len(self.sightings)

        # Initialize base map centered dynamically
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=9, tiles="OpenTopoMap")

        # Plot Protected Zones using the GeoJSON bridge method
        for z in self.zones:
            folium.GeoJson(
                z.to_geojson(),  # Pass the dictionary straight in
                style_function=lambda feature: {
                    'fillColor': '#2e7d32', 
                    'color': '#1b5e20', 
                    'weight': 2, 
                    'fillOpacity': 0.25
                },
                tooltip=folium.Tooltip(f"Sanctuary: {z.name}")
            ).add_to(m)

        # Plot Sighting Markers
        for s in self.sightings:
            marker_color = "red" if s.is_endangered else "blue"
            popup_html = f"""
            <b>Species:</b> {s.species} <br>
            <b>Count:</b> {s.count} <br>
            <b>Endangered:</b> {'Yes' if s.is_endangered else 'No'} <br>
            <b>Time:</b> {s.timestamp}
            """
            folium.Marker(
                location=[s.lat, s.lon],
                popup=folium.Popup(popup_html, max_width=200),
                icon=folium.Icon(color=marker_color, icon="info-sign")
            ).add_to(m)

        # Save output to an HTML file
        m.save(output_file)
        print(f"Interactive map successfully saved to '{output_file}'.")

if __name__ == "__main__":
    #print("Running Phase 1 Self-Test")
    
    #original_sighting = Sighting("snow leopard", lat=33.91, lon=77.45, count=1, is_endangered=True)
    # print("1. __str__ Output:")
    # print(original_sighting)
    
    # print("\n" + "-"*40 + "\n")
    
    # sighting_dict = original_sighting.to_dict()
    # print("2. to_dict() Output:")
    # print(sighting_dict)
    
    # print("\n" + "-"*40 + "\n")

    # recreated_sighting = Sighting.from_dict(sighting_dict)
    # print("3. Recreated Sighting from_dict():")
    # print(recreated_sighting)
    
    # print("\nValidation Checks:")
    # print(f"Species match: {original_sighting.species == recreated_sighting.species}")
    # print(f"Timestamp match: {original_sighting.timestamp == recreated_sighting.timestamp}")
    
    # print("Running Phase 2 Self-Test")
    # tracker = WildlifeTracker("sightings.json")

    # # -------------------------------------------------------------------------
    # # Run 1 - Log a new sighting (comment this out for Run 2 test)
    # # -------------------------------------------------------------------------
    # # tracker.log_sighting(Sighting("Snow Leopard", lat=33.91, lon=77.45, count=1, is_endangered=True))
    # # tracker.log_sighting(Sighting("Himalayan Blue Sheep", lat=33.85, lon=77.50, count=12, is_endangered=False))

    # # -------------------------------------------------------------------------
    # # Run 2 - Verifying data reload from JSON
    # # (After running once, comment out the tracker.log_sighting(...) above and rerun)
    # # -------------------------------------------------------------------------
    # print("\n--- Reloaded Sightings in Tracker ---")
    # print(tracker.sightings)
    # if tracker.sightings:
    #     print(f"First item species: {tracker.sightings[0].species}")
    
    # # -------------------------------------------------------------------------
    # -----Demonstration Run-----
    # # -------------------------------------------------------------------------
    tracker = WildlifeTracker()
    # Irregular multi-vertex polygon reserve boundary (longitude, latitude order)
    reserve_coords = [
        (77.20, 33.75),
        (77.60, 33.70),
        (77.85, 34.10),
        (77.50, 34.30),
        (77.15, 34.05),
        (77.20, 33.75)  # Closing the loop
    ]
    sanctuary = ProtectedZone("Markhor High Altitude Reserve", reserve_coords)
    tracker.add_zone(sanctuary)
    
    # Log test observations
    tracker.log_sighting(Sighting("Snow Leopard", lat=34.00, lon=77.45, count=1, is_endangered=True))
    tracker.log_sighting(Sighting("Himalayan Blue Sheep", lat=33.85, lon=77.50, count=15, is_endangered=False))

    # Export the interactive HTML map
    tracker.export_interactive_map("wildlife_polygon_map.html")


    tracker = WildlifeTracker("data/sightings.json")
    mapper = MapExporter()
    cli = WildlifeCli(tracker, mapper)
    cli.run()


