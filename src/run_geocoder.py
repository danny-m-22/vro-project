"""
run_geocoder.py

Reads a CSV file containing addresses, uses the geocoder module to batch geocode
these addresses into coordinates, and writes the results to a new CSV file.

Input:
    - data/addresses_sample.csv : CSV file with a "Full Address" column

Output:
    - data/coordinates.csv : CSV file with columns "Address" and "Coordinates" ([lon, lat])
"""

def main():
    import utils.geocoder as geocoder
    import os
    import pandas as pd

    # Define input and output file paths relative to project root
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    input_file = os.path.join(data_dir, "addresses_sample.csv")
    output_file = os.path.join(data_dir, "coordinates.csv")

    # Read addresses from CSV
    df = pd.read_csv(input_file)

    # Geocode addresses in batch, returning list of (address, coordinates) tuples
    results = geocoder.batch_geocode(df["Full Address"].to_list())

    # Convert results to DataFrame and save as CSV
    output_df = pd.DataFrame(results, columns=["Address", "Coordinates"])
    output_df.to_csv(output_file, index=False)

    print("Created coordinates.csv in data directory")


if __name__ == "__main__":
    main()
