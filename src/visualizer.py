"""
visualizer.py

Generates an interactive HTML map of the best vehicle routing path using Folium.
Each stop is marked, and each segment is color coded.

Input:
    - data/best_path.csv : CSV file with lat, lon, address, and time-to-next data

Output:
    - data/route_map.html : HTML map showing the optimal route
"""

import folium
import pandas as pd
import os
import requests


def load_coordinates(path):
    """
    Load coordinates and route metadata from CSV.

    Args:
        path (str): Path to CSV file containing best route info

    Returns:
        list: List of [lat, lon] coordinate pairs
        pd.DataFrame: Full DataFrame for marker labeling
    """
    df = pd.read_csv(path)
    lat_list = df['lat'].to_list()
    lon_list = df['lon'].to_list()
    coordinates = [[lat, lon] for lat, lon in zip(lat_list, lon_list)]
    return coordinates, df


def get_shortest_route(start_lat, start_lon, end_lat, end_lon):
    """
    Get list of coordinates for each step in order to draw a route.

    Args:
        start_lat: lat of current index
        start_lon: lon of current index
        end_lat: lat of next index
        end_lon: lon of next index

    Returns:
        route_coordinates: fully detailed list of coordinates
    """
    url = f'http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson'

    response = requests.get(url)
    data = response.json()
    route = data['routes'][0]['geometry']['coordinates']
    route_coordinates = [(coord[1], coord[0]) for coord in route]

    return route_coordinates


def add_markers(route_map, coordinates, df):
    """
    Add markers for each stop on the map with color coding and popups.

    Args:
        route_map (folium.Map): Folium map object to add markers to
        coordinates (list): List of [lat, lon] pairs
        df (pd.DataFrame): DataFrame with address and time-to-next info
    """
    for index, coord in enumerate(coordinates):
        if index == 0:
            color = "green"  # First stop
        elif index == len(coordinates) - 2:
            color = "red"    # Last stop
        elif index == len(coordinates) - 1:
            break            # Do not display return-to-start marker
        else:
            color = "blue"

        popup_text = (
            f"#{index + 1}<br><br>"
            f"{(df.iloc[index, 0].split(','))[0]}<br><br>"
            f"{df.iloc[index, 3]} s to next"
        )

        folium.Marker(
            location=coord,
            popup=folium.Popup(popup_text, width=300),
            icon=folium.Icon(color=color)
        ).add_to(route_map)


def build_map(coordinates):
    """
    Initialize and return a Folium map centered on the first coordinate.

    Args:
        coordinates (list): List of [lat, lon] pairs

    Returns:
        folium.Map: Initialized map object
    """
    return folium.Map(location=coordinates[0], zoom_start=12, tiles='CartoDB positron')


def draw_route(route_map, path_coordinates):
    """
    Add routes connecting all route coordinates to the map.

    Args:
        route_map (folium.Map): Map object to add polyline to
        path_coordinates (list): List of [lat, lon] pairs
    """
    colors = [
        'red', 'blue', 'green', 'purple', 'orange',
        'darkred', 'cadetblue', 'darkgreen', 'darkblue', 'black'
    ]

    for index, segment in enumerate(path_coordinates):
        # Use modulo just in case the list size changes later
        color = colors[index % len(colors)]

        folium.PolyLine(
            locations=segment,
            color=color,
            weight=5,
            opacity=0.8,
            popup=f"Segment {index + 1}"
        ).add_to(route_map)


def save_map(route_map, output_path):
    """
    Save the map to an HTML file.

    Args:
        route_map (folium.Map): Map object to save
        output_path (str): Destination file path
    """
    route_map.save(output_path)


def main():
    # Define file paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "best_path.csv")
    output_file = os.path.join(base_dir, "data", "route_map.html")

    # Load coordinates and metadata
    coordinates, df = load_coordinates(input_file)

    path_coordinates = []
    for index in range(len(coordinates)-1):
        coords_list = get_shortest_route(coordinates[index][0],
                           coordinates[index][1],
                           coordinates[index+1][0],
                           coordinates[index+1][1]
                           )
        path_coordinates.append(coords_list)

    # Build map and add content
    route_map = build_map(coordinates)
    add_markers(route_map, coordinates, df)
    draw_route(route_map, path_coordinates)

    # Save to HTML file
    save_map(route_map, output_file)
    print("Map made")


if __name__ == "__main__":
    main()
