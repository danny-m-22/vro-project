import pandas as pd
from geocoder import batch_geocode

address_df = pd.read_csv('data/addresses_sample.csv')
address_list = address_df['Full Address'].tolist()

results = batch_geocode(address_list)

for address, coords in results:
    print(f"{address} -> {coords}")

coordinates_df = pd.DataFrame(results, columns=['Full Address', 'Coordinates'])
coordinates_df.to_csv('../data/coordinates.csv', index=False)