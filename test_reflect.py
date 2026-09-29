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

question = """
A new Payment API SEV-1 incident has occurred.

Symptoms:
- HTTP 503 errors
- Database connection usage is at 100%
- The database connection pool was changed from 50 to 10
- A recent deployment payment-api-v3.1.0 occurred

Based on historical incidents in memory:

1. What is the most likely root cause?
2. Which remediation has previously worked?
3. Which remediation has previously failed?
4. What evidence from historical incidents supports the recommendation?
"""

print("=" * 60)
print("HINDSIGHT REFLECT TEST")
print("=" * 60)

try:
    response = client.reflect(
        bank_id=BANK_ID,
        query=question
    )

    print("\nHindsight analysis:\n")
    print(response.text)

except Exception as error:
    print("\nREFLECT FAILED")
    print(type(error).__name__)
    print(str(error))

print("\n" + "=" * 60)