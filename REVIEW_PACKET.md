# PRAVAH REVIEW PACKET

## Entry Point
GitHub Actions pipeline

## System Role
Pravah = Observability + Signal Routing

## Flow
CI → Metrics → Signal → Log

## Signal Schema
(trace_id, signal_type, severity, metrics, recommended_action)

## Trace Continuity
Same trace_id across:
- CI logs
- Pravah logs
- Signal output

## Cases
- Normal → anomaly_detected
- Failure → deployment_failure

## Isolation Proof
Pravah:
- does NOT execute
- does NOT decide
- does NOT call executer

## Final Statement
Pravah does NOT execute actions.