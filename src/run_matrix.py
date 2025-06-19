def main():
    from utils.matrix_builder import build_distance_matrix
    import os
    import pandas as pd
    import json

    print("Entered run_matrix.main()")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "coordinates.csv")

    df = pd.read_csv(input_file)

    # convert lon and lat from one string to 2 separate floats
    df[['lon', 'lat']] = df['Coordinates'].str.split(',', expand=True)

    df['lon'] = (df['lon'].str[1:]).str.strip()
    df['lat'] = (df['lat'].str[0:-1]).str.strip()

    df['lon'] = df['lon'].astype(float)
    df['lat'] = df['lat'].astype(float)

    # create 2D list
    lon_list = df['lon'].to_list()
    lat_list = df['lat'].to_list()

    coordinates_list = []
    for i in range(len(lon_list)):
        coordinates_list.append([lon_list[i], lat_list[i]])
    # function call
    results = build_distance_matrix(coordinates_list)

    print("Distance matrix created and stored in cache")


    # JSON to CSV
    second_input_file = os.path.join(base_dir, "cache", "distance_matrix.json")
    output_file = os.path.join(base_dir, "data", "durations.csv")

    with open(second_input_file, "r") as f:
        matrix_data = json.load(f)

    duration_matrix = matrix_data["durations"]
    matrix_df = pd.DataFrame(duration_matrix)

    matrix_df.to_csv(output_file)
    print("Distance matrix stored as csv")


if __name__ == "__main__":
    main()