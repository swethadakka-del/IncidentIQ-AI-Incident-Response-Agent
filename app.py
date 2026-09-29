import streamlit as st
from hindsight_client import Hindsight
from dotenv import load_dotenv
import os
import time


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = "incident-response-agent"
HINDSIGHT_URL = "https://api.hindsight.vectorize.io"

if not API_KEY:
    st.error(
        "HINDSIGHT_API_KEY was not found. "
        "Please check your .env file."
    )
    st.stop()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Incident Command Center",
    page_icon="🚨",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0b1020;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .incident-header {
        padding: 24px;
        border-radius: 14px;
        background: linear-gradient(
            135deg,
            #111827,
            #1e293b
        );
        border: 1px solid #475569;
        margin-bottom: 22px;
    }

    .incident-header h1 {
        color: #ffffff !important;
        margin-bottom: 8px;
    }

    .incident-header p {
        color: #cbd5e1 !important;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .metric-card {
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #334155;
        text-align: center;
    }

    .memory-card {
        padding: 20px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #334155;
        margin-bottom: 12px;
    }

    .success-box {
        padding: 15px;
        border-radius: 10px;
        background: #052e1b;
        border: 1px solid #166534;
        color: #dcfce7;
    }

    .warning-box {
        padding: 15px;
        border-radius: 10px;
        background: #3b2500;
        border: 1px solid #a16207;
        color: #fef3c7;
    }

    .danger-box {
        padding: 15px;
        border-radius: 10px;
        background: #3b0a0a;
        border: 1px solid #991b1b;
        color: #fee2e2;
    }

    .before-box {
        padding: 20px;
        border-radius: 12px;
        background: #172033;
        border: 1px solid #475569;
        min-height: 150px;
    }

    .after-box {
        padding: 20px;
        border-radius: 12px;
        background: #052e1b;
        border: 1px solid #166534;
        min-height: 150px;
    }

    .memory-arrow {
        text-align: center;
        font-size: 2rem;
        padding-top: 55px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HINDSIGHT HELPERS
# ============================================================

def create_hindsight_client():
    """
    Create a Hindsight client with a generous timeout.

    The client is created per operation and closed automatically
    using a context manager.
    """
    return Hindsight(
        base_url=HINDSIGHT_URL,
        api_key=API_KEY,
        timeout=300.0
    )


def get_result_text(result):
    """
    Safely extract readable text from a Hindsight recall result.
    """
    if hasattr(result, "text"):
        return str(result.text)

    if hasattr(result, "content"):
        return str(result.content)

    if isinstance(result, dict):
        for key in ["text", "content", "memory", "value"]:
            if key in result:
                return str(result[key])

    return str(result)


def perform_recall(query, retries=2):
    """
    Run Hindsight recall with automatic client cleanup.
    """

    last_error = None

    for attempt in range(retries):

        try:
            with create_hindsight_client() as client:

                response = client.recall(
                    bank_id=BANK_ID,
                    query=query
                )

                if hasattr(response, "results"):
                    return response.results

                return []

        except Exception as e:

            last_error = e

            if attempt < retries - 1:
                time.sleep(2)

    raise last_error


def perform_reflect(query, retries=2):
    """
    Run Hindsight reflect with automatic client cleanup.
    """

    last_error = None

    for attempt in range(retries):

        try:
            with create_hindsight_client() as client:

                response = client.reflect(
                    bank_id=BANK_ID,
                    query=query
                )

                return response

        except Exception as e:

            last_error = e

            if attempt < retries - 1:
                time.sleep(2)

    raise last_error


def perform_retain(content):
    """
    Store new organizational learning in Hindsight.
    """

    with create_hindsight_client() as client:

        return client.retain(
            bank_id=BANK_ID,
            content=content
        )


# ============================================================
# INCIDENT DATA
# ============================================================

incident = {
    "id": "INC-1057",
    "service": "Payment API",
    "severity": "SEV-1",
    "error_rate": 38,
    "db_usage": 100,
    "deployment": "payment-api-v3.1.0",
    "pool_before": 50,
    "pool_current": 10,
    "status": "DEGRADED"
}


# ============================================================
# DEMO MEMORY BASELINE
# ============================================================

SEEDED_MEMORY_COUNT = 6


# ============================================================
# SESSION STATE
# ============================================================

if "investigated" not in st.session_state:
    st.session_state.investigated = False

if "approved" not in st.session_state:
    st.session_state.approved = False

if "remediated" not in st.session_state:
    st.session_state.remediated = False

if "retained" not in st.session_state:
    st.session_state.retained = False

if "memory_verified" not in st.session_state:
    st.session_state.memory_verified = False

if "recall_results" not in st.session_state:
    st.session_state.recall_results = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "retain_message" not in st.session_state:
    st.session_state.retain_message = None

if "verification_results" not in st.session_state:
    st.session_state.verification_results = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="incident-header">

        <h1>🚨 AI Incident Command Center</h1>

        <p>
            Autonomous Incident Investigation with
            Organizational Memory
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP INCIDENT INFORMATION
# ============================================================

st.subheader("🔴 Active Incident")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Incident",
        incident["id"]
    )

with col2:

    st.metric(
        "Service",
        incident["service"]
    )

with col3:

    st.metric(
        "Severity",
        incident["severity"]
    )

with col4:

    st.metric(
        "Status",
        incident["status"]
    )


# ============================================================
# LIVE SIGNALS
# ============================================================

st.subheader("📡 Live Signals")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "HTTP 503 Error Rate",
        f'{incident["error_rate"]}%'
    )

with col2:

    st.metric(
        "Database Usage",
        f'{incident["db_usage"]}%'
    )

with col3:

    st.metric(
        "DB Pool",
        f'{incident["pool_current"]}'
    )

with col4:

    st.metric(
        "Deployment",
        incident["deployment"]
    )


st.divider()


# ============================================================
# BEFORE / AFTER MEMORY OVERVIEW
# ============================================================

st.subheader("🧠 Hindsight Organizational Memory")

before_col, arrow_col, after_col = st.columns(
    [5, 1, 5]
)

with before_col:

    st.markdown(
        f"""
        <div class="before-box">

        <h3>BEFORE THIS INCIDENT</h3>

        <p>
        📚 Seeded historical experiences:
        <b>{SEEDED_MEMORY_COUNT}</b>
        </p>

        <p>
        ❌ No learning from INC-1057 yet
        </p>

        <p>
        The agent can recall previous
        organizational experiences.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with arrow_col:

    st.markdown(
        """
        <div class="memory-arrow">
        →
        </div>
        """,
        unsafe_allow_html=True
    )


with after_col:

    if st.session_state.retained:

        st.markdown(
            """
            <div class="after-box">

            <h3>AFTER THIS INCIDENT</h3>

            <p>
            ✅ INC-1057 learning retained
            </p>

            <p>
            🧠 Future incidents can recall
            this experience.
            </p>

            <p>
            Organizational memory has been updated.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="after-box">

            <h3>AFTER THIS INCIDENT</h3>

            <p>
            ⏳ Waiting for incident resolution
            and learning retention.
            </p>

            <p>
            The new experience will be stored
            after remediation.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# ============================================================
# INVESTIGATION
# ============================================================

st.subheader("🔎 AI Investigation")

investigate_button = st.button(
    "🧠 Investigate Incident",
    type="primary",
    use_container_width=True
)


if investigate_button:

    query = f"""
    Incident {incident['id']}.

    Service: {incident['service']}

    Severity: {incident['severity']}

    Symptoms:
    - HTTP 503 errors at {incident['error_rate']}%
    - Database connection usage at {incident['db_usage']}%
    - Database pool changed from
      {incident['pool_before']} to {incident['pool_current']}
    - Recent deployment:
      {incident['deployment']}

    Find historical incidents with similar symptoms,
    root causes, remediation actions and outcomes.

    Identify:
    1. Similar historical incidents
    2. Repeated root-cause patterns
    3. Successful remediation actions
    4. Failed remediation actions
    5. Preventative organizational learning
    """

    with st.spinner(
        "Querying Hindsight organizational memory..."
    ):

        try:

            # ------------------------------------------------
            # RECALL
            # ------------------------------------------------

            recall_results = perform_recall(query)

            st.session_state.recall_results = recall_results

            # ------------------------------------------------
            # REFLECT
            # ------------------------------------------------

            reflect_response = perform_reflect(query)

            st.session_state.analysis = reflect_response

            st.session_state.investigated = True

            st.success(
                "✓ Hindsight Recall + Reflect completed successfully."
            )

        except Exception as e:

            st.error(
                f"Investigation failed: {e}"
            )


# ============================================================
# SHOW INVESTIGATION RESULTS
# ============================================================

if st.session_state.investigated:

    # --------------------------------------------------------
    # REMOVE CURRENT INCIDENT FROM HISTORICAL EVIDENCE
    # --------------------------------------------------------

    historical_results = []

    for result in st.session_state.recall_results:

        result_text = get_result_text(result)

        if incident["id"] not in result_text:
            historical_results.append(result)


    # --------------------------------------------------------
    # TWO COLUMN LAYOUT
    # --------------------------------------------------------

    col1, col2 = st.columns([1, 1])


    # ========================================================
    # HINDSIGHT MEMORY
    # ========================================================

    with col1:

        st.markdown("### 🧠 Hindsight Memory")

        st.metric(
            "Historical Memory Matches",
            len(historical_results)
        )

        st.markdown(
            """
            <div class="success-box">

            ✓ RECALL completed successfully

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            "#### Historical Evidence"
        )

        if not historical_results:

            st.info(
                "No historical evidence was returned."
            )

        else:

            for index, result in enumerate(
                historical_results[:5]
            ):

                result_text = get_result_text(result)

                with st.expander(
                    f"Historical Match #{index + 1}"
                ):

                    st.write(result_text)


    # ========================================================
    # AI ANALYSIS
    # ========================================================

    with col2:

        st.markdown(
            "### 🤖 AI Root-Cause Analysis"
        )

        analysis = st.session_state.analysis

        if analysis:

            analysis_text = get_result_text(
                analysis
            )

            st.write(
                analysis_text
            )

        else:

            st.warning(
                "No reflection result available."
            )


        st.markdown(
            "#### 🎯 Recommended Runbook"
        )

        st.code(
            "DB-CONNECTION-POOL-ROLLBACK",
            language="text"
        )

        st.markdown(
            """
            <div class="warning-box">

            ⚠ Recommendation requires human approval.

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # EVIDENCE SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        "### 📌 Investigation Findings"
    )

    finding_col1, finding_col2, finding_col3 = st.columns(3)

    with finding_col1:

        st.markdown(
            """
            **Root Cause Pattern**

            Deployment-related database
            connection pool configuration
            changes repeatedly caused
            connection exhaustion.
            """
        )

    with finding_col2:

        st.markdown(
            """
            **Effective Remediation**

            Historical evidence shows
            `DB-CONNECTION-POOL-ROLLBACK`
            repeatedly succeeded.
            """
        )

    with finding_col3:

        st.markdown(
            """
            **Ineffective Remediation**

            Historical evidence includes
            an incident where
            `APPLICATION-RESTART`
            failed to resolve the
            underlying configuration problem.
            """
        )


# ============================================================
# HUMAN APPROVAL
# ============================================================

if st.session_state.investigated:

    st.divider()

    st.subheader(
        "👤 Human Approval Required"
    )

    st.write(
        "The AI has investigated the incident and "
        "identified a recommended remediation."
    )

    st.write(
        "**Recommended Action:** "
        "Rollback the problematic deployment and restore "
        "the previous database connection pool configuration."
    )

    col1, col2 = st.columns(2)

    with col1:

        approve = st.button(
            "✅ APPROVE SIMULATED REMEDIATION",
            use_container_width=True,
            disabled=st.session_state.approved
        )

    with col2:

        reject = st.button(
            "❌ REJECT",
            use_container_width=True,
            disabled=st.session_state.approved
        )


    if reject:

        st.session_state.approved = False

        st.error(
            "Remediation rejected by human operator."
        )


    if approve:

        st.session_state.approved = True

        st.success(
            "✓ Human operator approved the simulated remediation."
        )


# ============================================================
# SIMULATED REMEDIATION
# ============================================================

if st.session_state.approved:

    st.divider()

    st.subheader(
        "⚙️ Remediation Execution"
    )

    st.info(
        "DEMO MODE: No real production systems are modified."
    )

    if not st.session_state.remediated:

        progress = st.progress(0)

        steps = [
            "Stopping affected deployment",
            "Restoring previous DB configuration",
            "Restoring connection pool to 50",
            "Restarting affected service",
            "Checking service health"
        ]

        for i, step in enumerate(steps):

            st.write(
                f"✓ {step}"
            )

            progress.progress(
                int(
                    ((i + 1) / len(steps))
                    * 100
                )
            )

            time.sleep(0.25)

        st.session_state.remediated = True

        st.success(
            "✓ Simulated remediation completed."
        )


# ============================================================
# VERIFICATION
# ============================================================

if st.session_state.remediated:

    st.divider()

    st.subheader(
        "📊 Verification"
    )

    st.caption(
        "The following values are simulated for the demonstration."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Database Usage",
            "42%",
            "-58 percentage points"
        )

    with col2:

        st.metric(
            "HTTP 503 Error Rate",
            "0.4%",
            "-37.6 percentage points"
        )

    with col3:

        st.metric(
            "Service Status",
            "HEALTHY"
        )


    st.success(
        "✓ Incident recovery verified successfully."
    )


# ============================================================
# POSTMORTEM
# ============================================================

if st.session_state.remediated:

    st.divider()

    st.subheader(
        "📝 Incident Postmortem"
    )

    postmortem = f"""
Incident: {incident['id']}

Service:
{incident['service']}

Severity:
{incident['severity']}

Root Cause:
Incorrect database connection pool configuration
introduced during deployment {incident['deployment']}.

Evidence:
- HTTP 503 errors reached 38%
- Database connection usage reached 100%
- Connection pool changed from 50 to 10
- Historical incidents showed the same pattern

Successful Remediation:
DB-CONNECTION-POOL-ROLLBACK

Verification:
- Database usage reduced from 100% to 42%
- HTTP 503 error rate reduced from 38% to 0.4%
- Service returned to HEALTHY

Failed Historical Remediation:
APPLICATION-RESTART

Lesson:
Restarting the application alone may not resolve
configuration-driven database connection exhaustion.

Organizational Learning:
Future incidents with similar symptoms should
consider the database connection pool configuration
and recent deployments before attempting
application restart.
"""

    st.text_area(
        "Generated Postmortem",
        postmortem,
        height=330
    )


# ============================================================
# RETAIN LEARNING
# ============================================================

if st.session_state.remediated:

    st.divider()

    st.subheader(
        "🧠 Hindsight Learning"
    )

    if not st.session_state.retained:

        st.write(
            "The resolved incident can now become "
            "organizational memory for future incidents."
        )

        retain_button = st.button(
            "🧠 RETAIN THIS EXPERIENCE IN HINDSIGHT",
            type="primary",
            use_container_width=True
        )

        if retain_button:

            learning = f"""
Incident {incident['id']} occurred on the Payment API.

Incident Context:
Severity: {incident['severity']}
Deployment: {incident['deployment']}

Symptoms:
HTTP 503 errors reached 38%.
Database connection usage reached 100%.
Connection pool changed from 50 to 10.
The incident occurred after deployment
{incident['deployment']}.

Root Cause:
Incorrect database connection pool configuration
introduced during deployment.

Successful Remediation:
DB-CONNECTION-POOL-ROLLBACK.

Verification:
Database usage reduced from 100% to 42%.
HTTP 503 error rate reduced from 38% to 0.4%.
Service returned to HEALTHY.

Historical Learning:
Application restart alone previously failed for
a similar incident when the underlying database
configuration problem remained.

Lesson:
For Payment API incidents involving HTTP 503 errors
and database connection exhaustion after a deployment,
investigate connection pool configuration and consider
rollback before application restart.

Organizational Learning:
Validate database connection pool changes before
production deployment and use historical incident
evidence when investigating similar failures.
"""

            with st.spinner(
                "Retaining new organizational learning..."
            ):

                try:

                    perform_retain(
                        learning
                    )

                    st.session_state.retained = True

                    st.session_state.retain_message = (
                        "✓ Experience retained in Hindsight."
                    )

                    st.success(
                        "✓ Experience retained in Hindsight."
                    )

                except Exception as e:

                    st.error(
                        f"Failed to retain memory: {e}"
                    )

    else:

        st.success(
            "✓ INC-1057 learning has been retained in Hindsight."
        )


# ============================================================
# VERIFY RETAINED MEMORY
# ============================================================

if st.session_state.retained:

    st.divider()

    st.subheader(
        "🔎 Verify the Memory Update"
    )

    st.write(
        "This step demonstrates that the new incident "
        "experience can be recalled from organizational memory."
    )

    verify_button = st.button(
        "🔎 VERIFY RETAINED MEMORY",
        use_container_width=True,
        disabled=st.session_state.memory_verified
    )

    if verify_button:

        verification_query = f"""
        Retrieve the organizational memory for incident
        {incident['id']}.

        Verify the retained learning about:
        - Payment API
        - HTTP 503 errors
        - database connection exhaustion
        - deployment {incident['deployment']}
        - incorrect connection pool configuration
        - DB-CONNECTION-POOL-ROLLBACK
        - successful recovery
        """

        with st.spinner(
            "Searching Hindsight for the newly retained experience..."
        ):

            try:

                verification_results = perform_recall(
                    verification_query
                )

                st.session_state.verification_results = (
                    verification_results
                )

                found_incident = False

                for result in verification_results:

                    result_text = get_result_text(
                        result
                    )

                    if incident["id"] in result_text:

                        found_incident = True
                        break


                if found_incident:

                    st.session_state.memory_verified = True

                    st.success(
                        "✓ Hindsight successfully recalled "
                        f"the retained experience for {incident['id']}."
                    )

                else:

                    st.warning(
                        "Hindsight returned results, but the "
                        f"{incident['id']} identifier was not found "
                        "in the returned text. The memory may still "
                        "be indexing; try verification again shortly."
                    )

            except Exception as e:

                st.error(
                    f"Memory verification failed: {e}"
                )


    if st.session_state.memory_verified:

        st.markdown(
            """
            <div class="success-box">

            <h3>✓ MEMORY UPDATE VERIFIED</h3>

            <p>
            The resolved incident was retained and can now
            participate in future organizational recall.
            </p>

            <p>
            This closes the learning loop:
            <b>RECALL → REFLECT → REMEDIATE → RETAIN → RECALL</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        verification_results = (
            st.session_state.verification_results
        )

        if verification_results:

            st.markdown(
                "#### Recalled Learning"
            )

            shown = 0

            for result in verification_results:

                result_text = get_result_text(
                    result
                )

                if incident["id"] in result_text:

                    st.info(
                        result_text
                    )

                    shown += 1

                    if shown >= 2:
                        break


# ============================================================
# MEMORY STATUS
# ============================================================

st.divider()

st.subheader(
    "🔄 Organizational Memory Loop"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="memory-card">

        <h3>🔎 RECALL</h3>

        <p>
        Retrieve historical incidents
        and organizational experience.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="memory-card">

        <h3>🧠 REFLECT</h3>

        <p>
        Reason across organizational
        memory to identify patterns.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="memory-card">

        <h3>💾 RETAIN</h3>

        <p>
        Store new incident learning
        for future incidents.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FULL LEARNING LOOP
# ============================================================

st.markdown(
    """
    ### 🔁 Continuous Organizational Learning

    **NEW INCIDENT**
    ↓

    **RECALL**
    Historical organizational memory

    ↓

    **REFLECT**
    Cross-incident reasoning

    ↓

    **RECOMMEND**
    Evidence-backed remediation

    ↓

    **HUMAN APPROVAL**
    Human remains in control

    ↓

    **REMEDIATE**
    Simulated safe action

    ↓

    **VERIFY**
    Confirm recovery

    ↓

    **POSTMORTEM**
    Capture what happened

    ↓

    **RETAIN**
    Store the experience in Hindsight

    ↓

    **FUTURE INCIDENT**
    New incident can recall the learning
    """,
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "AI Incident Command Center • "
    "Hindsight-powered organizational memory • "
    "Demo mode • Human approval required"
)