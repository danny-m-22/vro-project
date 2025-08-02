"""
matrix_builder.py

Generates and caches a driving duration distance matrix for a list of coordinates
using the OpenRouteService API. If a cached matrix exists, it loads and returns that
instead of making an API call to reduce latency and API usage.

Input:
    - coordinates : List of [longitude, latitude] pairs representing locations

Output:
    - Distance matrix JSON response containing driving durations between locations
    - Cache saved to cache/distance_matrix.json
"""

import openrouteservice
import json
import os
from src.config import ORS_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "distance_matrix.json")


def load_matrix_cache():
    # Load cached distance matrix JSON if file exists; otherwise return None
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None


def save_matrix_cache(matrix_data):
    # Ensure cache directory exists, then write matrix data to JSON file
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(matrix_data, f, indent=2)


def build_distance_matrix(coordinates):
    # Return cached matrix if available to avoid redundant API calls
    cached = load_matrix_cache()
    if cached:
        print("Using cached matrix")
        return cached

    # If no cache, create OpenRouteService client and request distance matrix
    print("No cache found; calling API")
    client = openrouteservice.Client(key=ORS_API_KEY)

    result = client.distance_matrix(
        locations=coordinates,
        profile='driving-car',
        metrics=['duration'],  # Only request travel time (duration)
        units='m',             # Duration units in minutes
        resolve_locations=False,
        sources=list(range(len(coordinates))),      # All locations as sources
        destinations=list(range(len(coordinates)))  # All locations as destinations
    )

    # Save result to cache for future use
    save_matrix_cache(result)
    print("Saved matrix to cache")
    return result
