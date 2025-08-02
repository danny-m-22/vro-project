"""
sample_building_data.py

Reads NYC building data from a CSV file, filters for complete and valid address records,
narrows down by borough (Manhattan), samples 10 random addresses, formats them into
a standardized full address string, and saves the result to a CSV file.

Input:
    - bobaadr.txt : raw building data with address components

Output:
    - addresses_sample.csv : CSV file containing 10 formatted addresses

"""

import os
import pandas as pd

# Define file paths relative to this script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
input_file = os.path.join(data_dir, "bobaadr.txt")
output_file = os.path.join(data_dir, "addresses_sample.csv")

# Read raw building data
nyc_building_data = pd.read_csv(input_file)

# Filter out rows with missing key address components
nyc_building_data = nyc_building_data.dropna(subset=["lhnd", "stname", "zipcode"])

# Ensure house number column ('lhnd') contains non-empty strings
nyc_building_data = nyc_building_data[nyc_building_data["lhnd"].str.strip().str.len() > 0]

# Blank 'addrtype' indicates a real building address range (not used here, but noted)
# nyc_building_data[nyc_building_data['addrtype'].isna()]

# Optional: narrow data by ZIP code (uncomment if needed)
# nyc_building_data = nyc_building_data[nyc_building_data['zipcode'] == '11201']

# Narrow data to Manhattan borough only (boro code 1)
nyc_building_data = nyc_building_data[nyc_building_data['boro'] == 1]

# Sample 10 random addresses from filtered data
sample_building_data = nyc_building_data.sample(10).copy()

# Select relevant columns for address formatting
sample_building_data = sample_building_data[['lhnd', 'stname', 'zipcode']]

# Construct standardized full address string:
#   house number + street name (title case, normalized spaces) + city + state + zip
sample_building_data['Full Address'] = (
    sample_building_data['lhnd'].str.strip() +
    " " +
    sample_building_data['stname'].str.strip().str.title().str.replace(r'\s+', ' ', regex=True) +
    ", New York, NY " +
    sample_building_data['zipcode'].astype(str)
).str.strip()

# Keep only the formatted address column
sample_building_data = sample_building_data[['Full Address']]

# Save formatted addresses to CSV without index column
sample_building_data.to_csv(output_file, index=False)
