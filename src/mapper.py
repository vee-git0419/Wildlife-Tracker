import folium
   
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