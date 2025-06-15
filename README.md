The purpose of this project is to attempt to solve vehicle routing optimization problems. The user can input addresses as a CSV, and my aim is to find the fastest route to reach each destination. If I have time, I'll look into solving the problem with multiple vehicles, consider vehicle capacity, visualize the route, etc.

As for data preparation: raw address data was obtained from NYC Open Data ("Building Footprints").
A sampling script is included in `/scripts/sample_building_data.py`, which generates `data/addresses_sample.csv`.
Only the small sample file is versioned in this repository.