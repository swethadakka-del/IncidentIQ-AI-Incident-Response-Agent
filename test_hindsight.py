import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("HINDSIGHT_API_KEY")

if not api_key:
    raise RuntimeError("HINDSIGHT_API_KEY was not found in .env")

# Connect to Hindsight
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key
)

print("=" * 50)
print("HINDSIGHT CONNECTION TEST")
print("=" * 50)
print("API key found: YES")
print("Hindsight client created successfully!")
print("=" * 50)