# Vehicle Routing Optimization Tool

This tool calculates and visualizes an optimized route through a list of addresses using OpenRouteService's distance matrix API, a nearest-neighbor heuristic, and 2-opt refinement.

## Features

- Standardizes coordinates from raw address data

- Builds a travel time matrix via OpenRouteService

- Solves for a near-optimal tour using nearest neighbor plus 2-opt

- Outputs results to CSV and a Folium route map

<a href="https://danny-m-22.github.io/vro-project/data/route_map.html">
  <img width="1018" height="1392" alt="Interactive Route Map" src="https://github.com/user-attachments/assets/df681da6-4b44-4975-9ba4-827cf885c9e9" />
</a>
<p><em>Click the image above to view the interactive map.</em></p>

## Setup

1. Clone the repo.

2. Add your OpenRouteService API key to `src/config.py`:
 ```python
 ORS_API_KEY = "your-api-key"
 ```

3. Install the required Python packages by running this command in your terminal:
```bash
pip install -r requirements.txt
```

## Usage

Run the full pipeline by executing this command from the root project directory:
python main.py

This will load and clean input data, build and cache the duration matrix, solve the route, and export best_path.csv and route_map.html

## Project Workflow

1. Geocode Addresses:
Run run_geocoder.py to convert input addresses (data/addresses_sample.csv) into geographic coordinates. The results are saved as data/coordinates.csv

2. Build Distance Matrix:
Run run_matrix.py to create a travel duration matrix between all coordinate points using the OpenRouteService API. The matrix is cached in cache/distance_matrix.json and saved as data/durations.csv

3. Solve Vehicle Routing Problem:
Run src/vrp.py to compute an optimized route using the duration matrix. The best route and associated times are saved to data/best_path.csv

4. Visualize Route:
Run src/visualizer.py to generate an interactive map (data/route_map.html) showing the optimized path with markers and travel times

## File Structure

- main.py — orchestrates the pipeline

- src/vrp.py — solver logic (nearest neighbor + 2-opt)

- src/visualizer.py — builds map from results

- utils/ — preprocessing and matrix builder

- data/ — input and output data

- cache/ — cached API responses

## Notes

- Assumes a single vehicle doing a round trip

- Assumes symmetric travel times

- Requires precomputed duration matrix; does not call ORS during runtime

## To Do

- Add multivehicle support

- Add command-line arguments for customization

- Add robustness checks for missing/invalid data
