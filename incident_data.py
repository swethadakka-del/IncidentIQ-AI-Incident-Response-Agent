incidents = [
    {
        "incident_id": "INC-1001",
        "service": "Payment API",
        "severity": "SEV-1",
        "symptoms": [
            "HTTP 503 errors",
            "Database connection pool exhausted"
        ],
        "deployment": "payment-api-v2.8.1",
        "root_cause": "Incorrect database connection pool configuration",
        "remediation": "Rollback deployment and restore previous configuration",
        "runbook": "DB-CONNECTION-POOL-ROLLBACK",
        "outcome": "Successful"
    },

    {
        "incident_id": "INC-1002",
        "service": "Payment API",
        "severity": "SEV-1",
        "symptoms": [
            "HTTP 503 errors",
            "Maximum database connections reached"
        ],
        "deployment": "payment-api-v2.9.0",
        "root_cause": "Incorrect database pool configuration",
        "remediation": "Rollback deployment",
        "runbook": "DB-CONNECTION-POOL-ROLLBACK",
        "outcome": "Successful"
    },

    {
        "incident_id": "INC-1003",
        "service": "Payment API",
        "severity": "SEV-1",
        "symptoms": [
            "HTTP 503 errors",
            "Connection pool exhaustion"
        ],
        "deployment": "payment-api-v3.0.1",
        "root_cause": "Incorrect production pool configuration",
        "remediation": "Rollback deployment",
        "runbook": "DB-CONNECTION-POOL-ROLLBACK",
        "outcome": "Successful"
    },

    {
        "incident_id": "INC-1004",
        "service": "Order API",
        "severity": "SEV-2",
        "symptoms": [
            "Request timeouts",
            "Database connection saturation"
        ],
        "deployment": "order-api-v1.8.2",
        "root_cause": "Database connection limit misconfiguration",
        "remediation": "Restore previous database configuration",
        "runbook": "DB-CONNECTION-POOL-ROLLBACK",
        "outcome": "Successful"
    },

    {
        "incident_id": "INC-1005",
        "service": "Payment API",
        "severity": "SEV-1",
        "symptoms": [
            "HTTP 503 errors",
            "High database connection usage"
        ],
        "deployment": "payment-api-v3.0.5",
        "root_cause": "Deployment introduced incorrect connection pool settings",
        "remediation": "Rollback deployment",
        "runbook": "DB-CONNECTION-POOL-ROLLBACK",
        "outcome": "Successful"
    },

    {
        "incident_id": "INC-1006",
        "service": "Payment API",
        "severity": "SEV-1",
        "symptoms": [
            "HTTP 503 errors",
            "Database timeout errors"
        ],
        "deployment": "payment-api-v2.7.4",
        "root_cause": "Database connection pool exhausted",
        "remediation": "Restart application",
        "runbook": "APPLICATION-RESTART",
        "outcome": "Failed"
    }
]