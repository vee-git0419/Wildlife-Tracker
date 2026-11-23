from datetime import datetime
from shapely.geometry import Point, Polygon
from shapely.geometry import mapping

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