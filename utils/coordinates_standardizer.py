def main():
    import os
    import pandas as pd

    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "coordinates.csv")

    df = pd.read_csv(input_file)
    df[['lon', 'lat']] = df['Coordinates'].str.split(',', expand=True)
    df = df.drop('Coordinates', axis=1)
    df['lon'],  df['lat'] = (df['lon'].str[1:]).str.strip(),  (df['lat'].str[0:-1]).str.strip()
    df['lon'], df['lat']  = df['lon'].astype(float), df['lat'].astype(float)
    return df

if __name__ == "__main__":
    coordinates_standardized = main()