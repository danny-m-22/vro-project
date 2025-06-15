from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

ORS_API_KEY = os.getenv("ORS_API_KEY")

if ORS_API_KEY is None:
    raise ValueError("ORS_API_KEY not set. Check your .env file.")