import time
from mitra import calculate_score
from sovereign_bridge import send_to_sarathi
from core import execute
from bucket import log_event
from outcome import record_outcome
import uuid


def process(metrics):
    trace_id = str(uuid.uuid4())

    log_event(trace_id, "monitor", metrics)

    # Proposal
    proposal = {
        "trace_id": trace_id,
        "action": "scale_up" if metrics["cpu"] > 0.7 else "none",
        "metrics": metrics
    }

    log_event(trace_id, "proposal_created", proposal)

    # Mitra scoring
    score_data = calculate_score(metrics)
    proposal.update(score_data)

    log_event(trace_id, "proposal_scored", score_data)

    # Approval (auto for now)
    log_event(trace_id, "proposal_approved", proposal)

    # Sarathi decision
    decision = send_to_sarathi(proposal)
    log_event(trace_id, "sarathi_decision", decision)

    if decision.get("status") == "BLOCK":
        return {"status": "blocked"}

    if decision.get("status") == "ESCALATE":
        return {"status": "needs_manual_approval"}

    # Core execution
    start = time.time()
    result = execute(proposal)
    latency = time.time() - start

    log_event(trace_id, "execution_result", result)

    # Outcome
    outcome = record_outcome(trace_id, result["status"] == "success", latency)
    log_event(trace_id, "outcome", outcome)

    return result