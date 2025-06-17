def main():
    from utils.matrix_builder import build_distance_matrix
    import os
    import pandas as pd

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

    print(df.head())

    # create 2D list
    lon_list = df['lon'].to_list()
    lat_list = df['lat'].to_list()

    coordinates_list = []
    for i in range(len(lon_list)):
        coordinates_list.append([lon_list[i], lat_list[i]])
    print("Loaded coordinates:", coordinates_list)
    # function call
    results = build_distance_matrix(coordinates_list)


    print("Distance matrix created and stored in cache")

if __name__ == "__main__":
    main()