# run_geocoder.py
def main():
    from utils.geocoder import batch_geocode
    import pandas as pd

    df = pd.read_csv("data/addresses.csv")
    address_list = df["Full Address"].tolist()

    results = batch_geocode(address_list)

    output_df = pd.DataFrame(results, columns=["Address", "Coordinates"])
    output_df.to_csv("data/coordinates.csv", index=False)

if __name__ == "__main__":
    main()
