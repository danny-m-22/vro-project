def main():
    from utils.geocoder import batch_geocode
    import os
    import pandas as pd

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    input_file = os.path.join(data_dir, "addresses_sample.csv")
    output_file = os.path.join(data_dir, "coordinates.csv")

    df = pd.read_csv(input_file)

    results = batch_geocode(df)

    output_df = pd.DataFrame(results, columns=["Address", "Coordinates"])
    output_df.to_csv(output_file, index=False)
    print("Created coordinates.csv in data directory")

if __name__ == "__main__":
    main()