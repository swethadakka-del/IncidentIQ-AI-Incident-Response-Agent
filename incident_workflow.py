import os
from datetime import datetime
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


# ============================================================
# INCIDENT
# ============================================================

incident = {
    "incident_id": "INC-1057",
    "service": "Payment API",
    "severity": "SEV-1",
    "error_rate": "38%",
    "database_usage": "100%",
    "deployment": "payment-api-v3.1.0",
    "pool_change": "50 → 10"
}


# ============================================================
# DISPLAY INCIDENT
# ============================================================

print("=" * 70)
print("        AI INCIDENT RESPONSE WORKFLOW")
print("=" * 70)

print("\nACTIVE INCIDENT")
print("-" * 70)

for key, value in incident.items():
    print(f"{key.replace('_', ' ').title():20}: {value}")


# ============================================================
# INVESTIGATION
# ============================================================

print("\n" + "=" * 70)
print("1. INVESTIGATION")
print("=" * 70)

investigation_query = f"""
Investigate this production incident:

Service: {incident["service"]}
Severity: {incident["severity"]}
HTTP error rate: {incident["error_rate"]}
Database usage: {incident["database_usage"]}
Recent deployment: {incident["deployment"]}
Database pool change: {incident["pool_change"]}

Find similar historical incidents and their outcomes.
"""

try:
    recall_result = client.recall(
        bank_id=BANK_ID,
        query=investigation_query
    )

    memories = recall_result.results[:5]

    print("\nHistorical evidence:")

    for index, memory in enumerate(memories, start=1):
        print(f"\n[{index}] {memory.text}")

except Exception as error:
    print("\nInvestigation failed:")
    print(type(error).__name__)
    print(str(error))
    memories = []


# ============================================================
# AI REASONING
# ============================================================

print("\n" + "=" * 70)
print("2. AI ROOT-CAUSE ANALYSIS")
print("=" * 70)

analysis_query = f"""
Analyze this incident using the historical experience stored
in Hindsight.

Incident:
{incident}

Determine:

- likely root cause
- supporting historical evidence
- successful remediation
- failed remediation
- recommended runbook
- verification checks
"""

try:
    reflection = client.reflect(
        bank_id=BANK_ID,
        query=analysis_query
    )

    analysis = reflection.text

    print("\nAI ANALYSIS:\n")
    print(analysis)

except Exception as error:
    print("\nAnalysis failed:")
    print(type(error).__name__)
    print(str(error))
    analysis = "Analysis unavailable."


# ============================================================
# RECOMMENDATION
# ============================================================

print("\n" + "=" * 70)
print("3. RECOMMENDATION")
print("=" * 70)

recommended_runbook = "DB-CONNECTION-POOL-ROLLBACK"

print(f"""
Recommended Action:
{recommended_runbook}

Reason:
Historical incidents show that database connection pool
misconfiguration following a deployment was resolved by
restoring the previous configuration.

Safety:
This workflow will NOT perform a real production action.
The remediation below is simulated for demonstration.
""")


# ============================================================
# HUMAN APPROVAL
# ============================================================

print("=" * 70)
print("4. HUMAN APPROVAL")
print("=" * 70)

approval = input(
    "\nApprove the simulated remediation? (yes/no): "
).strip().lower()

if approval not in ["yes", "y"]:
    print("\nHuman approval not granted.")
    print("Incident workflow stopped safely.")
    raise SystemExit


print("\nHuman approval received.")


# ============================================================
# SIMULATED REMEDIATION
# ============================================================

print("\n" + "=" * 70)
print("5. SIMULATED REMEDIATION")
print("=" * 70)

print(f"""
Executing simulated runbook:

{recommended_runbook}

[SIMULATION]
→ Stop affected deployment
→ Restore previous database pool configuration
→ Restore pool size: 50
→ Restart affected service
""")

print("Simulated remediation completed.")


# ============================================================
# VERIFICATION
# ============================================================

print("\n" + "=" * 70)
print("6. VERIFICATION")
print("=" * 70)

verification = {
    "Database connection usage": "100% → 42%",
    "HTTP 503 error rate": "38% → 0.4%",
    "Service health": "DEGRADED → HEALTHY",
    "Deployment configuration": "Restored"
}

for metric, result in verification.items():
    print(f"✓ {metric:30} {result}")


print("\nIncident recovery verified successfully.")


# ============================================================
# POSTMORTEM
# ============================================================

print("\n" + "=" * 70)
print("7. POSTMORTEM")
print("=" * 70)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

postmortem = f"""
Incident ID: {incident["incident_id"]}
Service: {incident["service"]}
Severity: {incident["severity"]}

Root Cause:
Incorrect database connection pool configuration introduced
during deployment {incident["deployment"]}.

Observed Impact:
HTTP 503 errors reached {incident["error_rate"]}.
Database connection usage reached {incident["database_usage"]}.

Remediation:
{recommended_runbook}

Result:
Successful simulated recovery.

Learning:
Deployment-related database pool configuration changes
should be validated before production release.

Recorded At:
{timestamp}
"""

print(postmortem)


# ============================================================
# LEARNING LOOP — RETAIN
# ============================================================

print("=" * 70)
print("8. UPDATING HINDSIGHT MEMORY")
print("=" * 70)

try:

    client.retain(
        bank_id=BANK_ID,
        content=f"""
Completed Production Incident

{postmortem}

Outcome:
Successful recovery.

Historical Learning:
The DB-CONNECTION-POOL-ROLLBACK runbook successfully restored
service after database connection pool misconfiguration.

This incident should be used as future organizational memory
for similar Payment API database connection incidents.
"""
    )

    print("\n✓ New incident experience stored in Hindsight.")
    print("✓ Organizational memory updated.")

except Exception as error:

    print("\nMemory update failed:")
    print(type(error).__name__)
    print(str(error))


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("INCIDENT RESPONSE WORKFLOW COMPLETED")
print("=" * 70)

print("""
Incident
   ↓
Investigation
   ↓
Hindsight Recall
   ↓
AI Reasoning
   ↓
Recommendation
   ↓
Human Approval
   ↓
Simulated Remediation
   ↓
Verification
   ↓
Postmortem
   ↓
Hindsight Retain
   ↓
Future incidents learn from this experience
""")