import openrouteservice
import json
import os
from src.config import ORS_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "distance_matrix.json")

# CHECK IF MATRIX FILE EXISTS
def load_matrix_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

# SAVE MATRIX
def save_matrix_cache(matrix_data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(matrix_data, f, indent=2)

# MAKE & SAVE MATRIX IF NOT ALREADY MADE
def build_distance_matrix(coordinates):
    cached = load_matrix_cache()
    if cached:
        print("Using cached matrix")
        return cached
    print("No cache found; calling API")

    client = openrouteservice.Client(key=ORS_API_KEY)

    result = client.distance_matrix(
        locations=coordinates,
        profile='driving-car',
        metrics=['duration'],
        units='m',
        resolve_locations=False,
        sources=list(range(len(coordinates))),
        destinations=list(range(len(coordinates)))
    )

    save_matrix_cache(result)
    print("Saved matrix to cache")
    return result
