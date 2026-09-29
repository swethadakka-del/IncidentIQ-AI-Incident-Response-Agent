import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")

if not API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY was not found in .env")

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=API_KEY
)

BANK_ID = "incident-response-agent"


# --------------------------------------------------
# NEW INCIDENT
# --------------------------------------------------

new_incident = {
    "incident_id": "INC-1057",
    "service": "Payment API",
    "severity": "SEV-1",
    "symptoms": [
        "HTTP 503 errors",
        "38% request failure rate",
        "Database connection usage at 100%"
    ],
    "deployment": "payment-api-v3.1.0",
    "database_pool": "50 → 10"
}


# --------------------------------------------------
# FORMAT INCIDENT FOR HINDSIGHT
# --------------------------------------------------

incident_text = f"""
New Production Incident

Incident ID: {new_incident["incident_id"]}
Service: {new_incident["service"]}
Severity: {new_incident["severity"]}

Symptoms:
{", ".join(new_incident["symptoms"])}

Recent Deployment:
{new_incident["deployment"]}

Database Connection Pool:
{new_incident["database_pool"]}
"""


# --------------------------------------------------
# RECALL
# --------------------------------------------------

print("=" * 70)
print("INCIDENT RESPONSE AGENT")
print("=" * 70)

print("\n[1] NEW INCIDENT")
print(incident_text)

print("\n[2] SEARCHING HINDSIGHT MEMORY...")

try:

    recall_result = client.recall(
        bank_id=BANK_ID,
        query=incident_text
    )

    print("\nHistorical evidence found:")

    for index, memory in enumerate(recall_result.results[:5], start=1):
        print(f"\n--- Historical Match {index} ---")
        print(memory.text)

except Exception as error:

    print("\nRECALL ERROR")
    print(type(error).__name__)
    print(str(error))


# --------------------------------------------------
# REFLECT
# --------------------------------------------------

print("\n" + "=" * 70)
print("[3] ANALYZING HISTORICAL EXPERIENCE")
print("=" * 70)

question = f"""
Analyze this new production incident:

{incident_text}

Use historical incidents stored in Hindsight memory.

Determine:

1. The most likely root cause.
2. The historical incidents supporting this conclusion.
3. Which remediation previously succeeded.
4. Which remediation previously failed.
5. The recommended runbook.
6. What evidence should be checked before taking action.
7. What verification should be performed after remediation.
"""

try:

    reflection = client.reflect(
        bank_id=BANK_ID,
        query=question
    )

    print("\nAGENT ANALYSIS:\n")
    print(reflection.text)

except Exception as error:

    print("\nREFLECT ERROR")
    print(type(error).__name__)
    print(str(error))


print("\n" + "=" * 70)
print("END OF INCIDENT ANALYSIS")
print("=" * 70)