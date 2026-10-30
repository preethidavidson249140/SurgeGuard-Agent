
from datetime import datetime, timezone


def verify_agent_request(
    patient_id,
    requested_patient_id,
    requested_scope,
    consent_scopes,
    consent_expires,
    agent_instruction=""
):
    """
    Educational simulation of a health-data consent guard.
    Uses fictional identifiers and permissions only.
    """

    reasons = []

    if patient_id != requested_patient_id:
        reasons.append("Patient identifier mismatch")

    if requested_scope not in consent_scopes:
        reasons.append("Requested data is outside consent scope")

    if datetime.now(timezone.utc) >= consent_expires:
        reasons.append("Consent has expired")

    # Untrusted instructions cannot override the checks above.
    # The instruction is not used to authorize access.

    if reasons:
        return {
            "decision": "BLOCK",
            "reasons": reasons
        }

    return {
        "decision": "ALLOW",
        "reasons": ["All configured consent checks passed"]
    }
