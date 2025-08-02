"""
geocoder.py

Uses OpenRouteService API to convert addresses into geographic coordinates.
Caches geocoded results locally in a JSON file to reduce API calls and improve efficiency.

Input:
    - List of addresses (strings) to geocode
    - ORS_API_KEY from config

Output:
    - List of tuples (address, [longitude, latitude]) or None if geocoding failed
    - Cache saved to cache/geocoded_addresses.json
"""

import openrouteservice
import json
import os
from src.config import ORS_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "geocoded_addresses.json")


def load_cache():
    # Load cached geocoded addresses from file if it exists, otherwise return empty dict
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    # Ensure cache directory exists, then write cache dictionary to JSON file
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def geocode_address(client, address, cache):
    # Return cached coordinates if available
    if address in cache:
        return cache[address]

    # Otherwise, query OpenRouteService API and cache the result
    try:
        result = client.pelias_search(text=address)
        coordinates = result["features"][0]["geometry"]["coordinates"]
        cache[address] = coordinates
        return coordinates
    except Exception as e:
        print(f"Failed to geocode: {address} -> {e}")
        return None


def batch_geocode(address_list):
    # Initialize ORS client with API key
    client = openrouteservice.Client(key=ORS_API_KEY)

    # Load existing cache to prevent redundant API calls
    cache = load_cache()

    coordinates_list = []
    for address in address_list:
        # Geocode each address and collect results
        coordinates = geocode_address(client, address, cache)
        coordinates_list.append((address, coordinates))

    # Save updated cache to disk
    print("Saved coordinates to cache")
    save_cache(cache)

    return coordinates_list
