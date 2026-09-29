from hindsight_client import Hindsight
from dotenv import load_dotenv
import os

from incident_data import incidents

load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")

if not api_key:
    raise RuntimeError("HINDSIGHT_API_KEY was not found in .env")

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key
)

BANK_ID = "incident-response-agent"


def format_incident(incident):
    symptoms = ", ".join(incident["symptoms"])

    return f"""
Historical Production Incident

Incident ID: {incident["incident_id"]}
Service: {incident["service"]}
Severity: {incident["severity"]}

Symptoms:
{symptoms}

Deployment:
{incident["deployment"]}

Root Cause:
{incident["root_cause"]}

Remediation:
{incident["remediation"]}

Runbook:
{incident["runbook"]}

Outcome:
{incident["outcome"]}
"""


print("=" * 60)
print("LOADING HISTORICAL INCIDENTS INTO HINDSIGHT")
print("=" * 60)

for incident in incidents:

    memory = format_incident(incident)

    try:
        client.retain(
            bank_id=BANK_ID,
            content=memory
        )

        print(
            f"✓ {incident['incident_id']} "
            f"stored successfully"
        )

    except Exception as error:

        print(
            f"✗ {incident['incident_id']} "
            f"failed"
        )

        print(f"  Error: {error}")

print()
print("Historical incident loading completed.")
print("=" * 60)