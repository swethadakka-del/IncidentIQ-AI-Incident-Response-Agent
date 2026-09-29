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

query = """
A Payment API deployment is causing HTTP 503 errors.
Database connections are exhausted.
The database connection pool configuration was recently changed.
Find similar historical incidents and explain which remediation
actions succeeded and which failed.
"""

print("=" * 60)
print("HINDSIGHT RECALL TEST")
print("=" * 60)

try:
    result = client.recall(
    bank_id=BANK_ID,
    query=query
)
    print("\nHistorical memories found:\n")

    for index, memory in enumerate(result.results, start=1):
        print(f"\n--- Match {index} ---")
        print(memory.text)

except Exception as error:
    print("\nRECALL FAILED")
    print(type(error).__name__)
    print(str(error))

print("\n" + "=" * 60)