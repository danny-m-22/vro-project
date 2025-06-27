import folium
import pandas as pd
import os

# TODO make a function w/ cvrp ouput as input

base_dir = os.path.dirname(os.path.dirname(__file__))
input_file = os.path.join(base_dir, "data", "coordinates.csv")
output_file = os.path.join(base_dir, "data", "route_map.html")

df = pd.read_csv(input_file)

# Clean & Reorganize Coordinates

df[['lon', 'lat']] = df['Coordinates'].str.split(',', expand=True)
df['lon'],  df['lat'] = (df['lon'].str[1:]).str.strip(),  (df['lat'].str[0:-1]).str.strip()
df['lon'], df['lat']  = df['lon'].astype(float), df['lat'].astype(float)
lon_list, lat_list = df['lon'].to_list(), df['lat'].to_list()

coordinates_list = []
for i in range(len(lon_list)):
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