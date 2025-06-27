import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
input_file = os.path.join(data_dir, "bobaadr.txt")
output_file = os.path.join(data_dir, "addresses_sample.csv")

nyc_building_data = pd.read_csv(input_file)
nyc_building_data[nyc_building_data['addrtype'].isna()]

# according to the documentation, blank address types indicate
# "real address range of a building on the tax lot."

# NARROW DATA BY ZIP CODE  #TODO Check zipcodes
nyc_building_data = nyc_building_data[nyc_building_data['zipcode'] == '11201']
# see data_documentation for more info on NYC zip codes


# NARROW DATA BY BOROUGH
#nyc_building_data = nyc_building_data[nyc_building_data['boro'] == '']
# from documentation:
# 1 = Manhattan, 2 = Bronx, 3 = Brooklyn, 4 = Queens, 5 = Staaten Island
# this is done to limit the area being looked at

# GET RANDOM ADDRESSES
sample_building_data = nyc_building_data.sample(10).copy()

# GET HOUSE NUMBER, STREET ADDRESS, AND ZIP CODE; CONCATENATE
sample_building_data = sample_building_data[['lhnd', 'stname', 'zipcode']]

sample_building_data['Full Address'] = (
        sample_building_data['lhnd'].str.strip() +
        " " +
        ((sample_building_data['stname'].str.strip()).str.title()).str.replace(r'\s+', ' ', regex=True)  +
        ", New York, NY " +
        sample_building_data['zipcode'].astype(str)
).str.strip()

sample_building_data = sample_building_data[['Full Address']]

# SAMPLE TO CSV
sample_building_data.to_csv(output_file, index=False)