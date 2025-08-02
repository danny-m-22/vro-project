"""
run_matrix.py

Generates a driving duration distance matrix for coordinates obtained from the
coordinates_standardizer module, caches the matrix, and exports the duration matrix
to a CSV file.

Input:
    - Coordinates loaded via coordinates_standardizer.main()
    - Cached distance matrix JSON (if exists) or generates new via API

Output:
    - Cache file: cache/distance_matrix.json
    - CSV file: data/durations.csv containing the duration matrix
"""

def main():
    from utils.matrix_builder import build_distance_matrix
    import os
    import pandas as pd
    import json
    from utils.coordinates_standardizer import main as standard_coords

    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Get standardized coordinates as DataFrame
    df = standard_coords()

    # Combine longitude and latitude into coordinate pairs
    lon_list, lat_list = df['lon'].to_list(), df['lat'].to_list()
    coordinates_list = []
    for i in range(len(lon_list)):
        coordinates_list.append([lon_list[i], lat_list[i]])

    # Build or load cached distance matrix using API
    results = build_distance_matrix(coordinates_list)
    print("Distance matrix created and stored in cache")

    # Load cached distance matrix JSON file
    second_input_file = os.path.join(base_dir, "cache", "distance_matrix.json")
    output_file = os.path.join(base_dir, "data", "durations.csv")

    with open(second_input_file, "r") as f:
        matrix_data = json.load(f)

    # Extract duration matrix and convert to DataFrame
    duration_matrix = matrix_data["durations"]
    matrix_df = pd.DataFrame(duration_matrix)

    # Save duration matrix as CSV for further use
    matrix_df.to_csv(output_file)
    print("Distance matrix stored as csv")


if __name__ == "__main__":
    main()
