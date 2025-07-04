import folium
import pandas as pd
import os
from utils.coordinates_standardizer import main as standard_coords

# TODO make a function w/ cvrp ouput as input

base_dir = os.path.dirname(os.path.dirname(__file__))
output_file = os.path.join(base_dir, "data", "route_map.html")

df = standard_coords()
lat_list, lon_list = df['lat'].to_list(), df['lon'].to_list()
coordinates_list = []
for i in range(len(lat_list)):
    coordinates_list.append([lat_list[i], lon_list[i]])


# Make Map #TODO add labels to coordinates: in addition to index, address and coordinates
route_map = folium.Map(location=coordinates_list[0], zoom_start=13)
for index, coord in enumerate(coordinates_list):
    folium.Marker(
        location=coord,
        # The popup will display the stop number. We add 1 because index starts at 0.
        popup=f"Stop #{index + 1}"
    ).add_to(route_map)

folium.PolyLine(
    locations=coordinates_list,
    color='blue',
    weight=5,
    opacity=0.8
).add_to(route_map)

route_map.save(output_file)

def main():
    print("")

if __name__ == "__main__":
    main()