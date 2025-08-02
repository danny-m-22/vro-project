"""
config.py

Loads environment variables from a .env file and provides access to
the OpenRouteService API key required for API requests.

Input:
    - .env file containing ORS_API_KEY variable

Output:
    - ORS_API_KEY string loaded into the module namespace
    - Raises an error if ORS_API_KEY is not found
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file into process environment
load_dotenv()

# Retrieve OpenRouteService API key from environment variables
ORS_API_KEY = os.getenv("ORS_API_KEY")

# Raise error if API key is not set to prevent silent failures
if ORS_API_KEY is None:
    raise ValueError("ORS_API_KEY not set. Check your .env file.")
