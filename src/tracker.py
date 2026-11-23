import json 
from shapely.geometry import Point, Polygon
from shapely.geometry import mapping
from src.models import Sighting, ProtectedZone

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
