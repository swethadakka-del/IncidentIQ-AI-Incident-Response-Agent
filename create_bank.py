import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")

if not api_key:
    raise RuntimeError("HINDSIGHT_API_KEY was not found in .env")

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key
)

BANK_ID = "incident-response-agent"

print("=" * 60)
print("CREATING INCIDENT RESPONSE MEMORY BANK")
print("=" * 60)

try:
    result = client.create_bank(
        bank_id=BANK_ID,
        name="Incident Response Agent"
    )

    print("\nSUCCESS!")
    print("Memory bank created:")
    print(BANK_ID)
    print("\nHindsight is ready for incident memories.")

except Exception as error:
    print("\nERROR:")
    print(type(error).__name__)
    print(str(error))

print("=" * 60)