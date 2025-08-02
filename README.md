# Vehicle Routing Optimization Tool

This tool calculates and visualizes an optimized route through a list of addresses using OpenRouteService's distance matrix API, a nearest-neighbor heuristic, and 2-opt refinement.

## Features

- Standardizes coordinates from raw address data

- Builds a travel time matrix via OpenRouteService

- Solves for a near-optimal tour using nearest neighbor plus 2-opt

- Outputs results to CSV and a Folium route map

## Setup

- Clone the repo.

- Add your OpenRouteService API key to the file src/config.py by adding this line:
ORS_API_KEY = "your-api-key"

- Install the required Python packages by running this command in your terminal:
pip install -r requirements.txt

## Usage

Run the full pipeline by executing this command from the root project directory:
python main.py

This will load and clean input data, build and cache the duration matrix, solve the route, and export best_path.csv and route_map.html.

## File Structure

- main.py — orchestrates the pipeline

- src/vrp.py — solver logic (nearest neighbor + 2-opt)

- src/visualizer.py — builds map from results

- utils/ — preprocessing and matrix builder

- data/ — input and output data

- cache/ — cached API responses