import folium
import pandas as pd
import os
from vrp import main as solver

base_dir = os.path.dirname(os.path.dirname(__file__))
output_file = os.path.join(base_dir, "data", "route_map.html")

df = solver()
lat_list, lon_list = df['lat'].to_list(), df['lon'].to_list()
coordinates_list = []
for i in range(len(lat_list)):
    coordinates_list.append([lat_list[i], lon_list[i]])
print(df)

route_map = folium.Map(location=coordinates_list[0], zoom_start=12, tiles='CartoDB positron')

for index, coord in enumerate(coordinates_list):
    if index == 0:
        color = "green"  # First stop
    elif index == len(coordinates_list) - 2:
        color = "red"    # Last stop
    elif index == len(coordinates_list) - 1:
        break
    else:
        color = "blue"


    folium.Marker(
        location=coord,
        popup=folium.Popup(
            f"#{index + 1}<br><br>{(df.iloc[index, 0].split(','))[0]}<br><br>{df.iloc[index, 3]} s to next",
            width=300
        ),
        icon=folium.Icon(color=color)
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