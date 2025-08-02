"""
coordinates_standardizer.py

Reads a CSV file containing coordinate data in string format,
parses the 'Coordinates' column into separate longitude and latitude
columns as floats, and returns the cleaned DataFrame.

Input:
    - coordinates.csv : CSV file with a 'Coordinates' column, formatted as "[lon, lat]"

Output:
    - DataFrame with separate 'lon' and 'lat' float columns
"""

def main():
    import os
    import pandas as pd

    # Define input file path relative to project root directory
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "coordinates.csv")

    # Load CSV data
    df = pd.read_csv(input_file)

    # Split the 'Coordinates' string column into two new columns: 'lon' and 'lat'
    df[['lon', 'lat']] = df['Coordinates'].str.split(',', expand=True)

    # Drop original 'Coordinates' column as it's no longer needed
    df = df.drop('Coordinates', axis=1)

    # Remove brackets and whitespace from 'lon' and 'lat' strings
    df['lon'] = df['lon'].str[1:].str.strip()    # Remove leading '['
    df['lat'] = df['lat'].str[:-1].str.strip()   # Remove trailing ']'

    # Convert 'lon' and 'lat' columns from strings to floats
    df['lon'] = df['lon'].astype(float)
    df['lat'] = df['lat'].astype(float)

    return df


if __name__ == "__main__":
    coordinates_standardized = main()
