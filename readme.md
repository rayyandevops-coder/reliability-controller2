# PRAVAH — Observability System

## Overview
Pravah is a signal-based observability layer.

It:
- detects
- measures
- emits signals

It does NOT:
- execute
- decide

## Architecture
CI → Pravah → Signal

## Endpoints
- /metrics
- /emit-signal
- /health

## Signals
- anomaly_detected
- deployment_failure
- latency_spike
- health_degradation

## Trace
trace_id maintained across system

## Output
Structured JSON signals

## Status
Production-ready (TANTRA compliant)