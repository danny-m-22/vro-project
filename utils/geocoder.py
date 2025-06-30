import openrouteservice
import json
import os
from src.config import ORS_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "geocoded_addresses.json")


# CHECK IF ADDRESS FILE EXISTS
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

# SAVE ADDRESS FILE
def save_cache(cache):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


# GEOCODE ONE ADDRESS
def geocode_address(client, address, cache):
    if address in cache:
        return cache[address]

    try:
        result = client.pelias_search(text=address)
        coordinates = result["features"][0]["geometry"]["coordinates"]
        cache[address] = coordinates
        return coordinates
    except Exception as e:
        print(f"Failed to geocode: {address} -> {e}")
        return None

# GEOCODE ALL ADDRESSES
def batch_geocode(address_list):
    client = openrouteservice.Client(key=ORS_API_KEY)
    cache = load_cache()
    coordinates_list = []

    for address in address_list:
        coordinates = geocode_address(client, address, cache)
        coordinates_list.append((address, coordinates))

    print("Saved coordinates to cache")
    save_cache(cache)
    return coordinates_list
