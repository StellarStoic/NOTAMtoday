import os
import folium
from pykml import parser
import geopandas as gpd

def extract_coordinates_from_kml(kml_file):
    """Extract coordinates from a KML file using pykml."""
    with open(kml_file, 'r', encoding='utf-8') as file:
        kml_content = parser.parse(file).getroot()
        coords = []
        center = None  # Initialize center

        for placemark in kml_content.Document.Placemark:
            # Extracting center from Point
            if hasattr(placemark, 'MultiGeometry') and hasattr(placemark.MultiGeometry, 'Point'):
                coord_text = placemark.MultiGeometry.Point.coordinates.text
                coord_pairs = coord_text.split(',')
                center = (float(coord_pairs[1]), float(coord_pairs[0]))  # Set center

            # Extracting coordinates from Polygon
            if hasattr(placemark, 'MultiGeometry') and hasattr(placemark.MultiGeometry, 'Polygon'):
                coord_text = placemark.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates.text
                coord_pairs = coord_text.split()
                coord_tuples = [(float(pair.split(',')[1]), float(pair.split(',')[0])) for pair in coord_pairs]
                coords.append(coord_tuples)

        return center, coords

def plot_map_with_coordinates(center, coordinates, filename):
    """Plot a map centered on a location with specific coordinates using folium."""
    
    # Create a folium map object
    m = folium.Map(location=center, tiles=None)

    # Add the OpenTopoMap tile layer
    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        min_zoom=10,
        name='OpenTopoMap'
    ).add_to(m)

    # Plot the NOTAM airspace coordinates with transparent red color
    
    for coord_list in coordinates:
        folium.Polygon(locations=coord_list, color='red', fill=True, fill_color='red', fill_opacity=0.35).add_to(m)
    
    # Compute the bounding box of the coordinates
    lats = [coord[0] for sublist in coordinates for coord in sublist]
    lons = [coord[1] for sublist in coordinates for coord in sublist]
    min_lat, max_lat, min_lon, max_lon = min(lats), max(lats), min(lons), max(lons)
    
    # Adjust the map view to fit the bounding box
    m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
    
    # Check the size of the bounding box
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon

    # If the bounding box is smaller than a certain threshold, expand the bounds
    
    '''Threshold Values (lat_diff and lon_diff):
These values determine the size of the NOTAM that will trigger the zoom-out effect.
If the NOTAM's size (in terms of latitude and longitude differences) is smaller than these threshold values, the map will zoom out.
Increasing these values means that larger NOTAMs will also trigger the zoom-out effect.
Decreasing these values means only very small NOTAMs will trigger the zoom-out effect.'''
    
    if lat_diff < 0.02 and lon_diff < 0.02:  # Adjust the threshold values as needed
        
        '''Expansion Factor (expansion_factor):
This value determines how much the map will zoom out when the zoom-out effect is triggered.
It does this by expanding the bounding box of the NOTAM by the specified factor.
Increasing the expansion factor will zoom out more, showing a larger area around the NOTAM.
Decreasing the expansion factor will zoom out less, showing a smaller area around the NOTAM.'''
        
        expansion_factor = 0.02  # Adjust this value as needed
        
        '''To summarize:
If you want the map to zoom out for larger NOTAMs as well, increase the threshold values.
If you want the map to zoom out more when it does, increase the expansion factor.
Conversely, if you want the map to zoom out only for very tiny NOTAMs, decrease the threshold values.
If you want the map to zoom out just a little bit when it does, decrease the expansion factor.'''

        min_lat -= expansion_factor
        max_lat += expansion_factor
        min_lon -= expansion_factor
        max_lon += expansion_factor
        m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    # Inject CSS to adjust the saturation of the OpenTopoMap tiles
    css = """
<style>
    .leaflet-tile-pane img.leaflet-tile { 
        filter: saturate(0.6);
    }
</style>
"""

    css_element = folium.Element(css)
    m.get_root().header.add_child(css_element)

    # Save the map as an HTML in the 'img' folder with the provided filename
    m.save(os.path.join('/home/NOTAMtoday/NOTAMtoday/HTMLs', filename + '.html'))



def main():
    # Path to the directory containing your KML files
    kml_directory = '/home/NOTAMtoday/NOTAMtoday/KMLs'
    
    # Ensure the 'HTMLs' directory exists or create it
    if not os.path.exists('/home/NOTAMtoday/NOTAMtoday/HTMLs'):
        os.makedirs('/home/NOTAMtoday/NOTAMtoday/HTMLs')
    
    for kml_file in os.listdir(kml_directory):
        if kml_file.endswith('.kml'):
            center, coords = extract_coordinates_from_kml(os.path.join(kml_directory, kml_file))
            plot_map_with_coordinates(center, coords, kml_file.split('.')[0])

if __name__ == "__main__":
    main()
