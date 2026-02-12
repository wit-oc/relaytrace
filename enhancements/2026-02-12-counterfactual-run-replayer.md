# Counterfactual Run Replayer (Enhancement)

Date: 2026-02-12
Status: Deferred enhancement (keep warm)
Primary track: Telemetry/KPI
Related tracks: Approval UX, Trust calibration, Policy tuning

## Why this belongs in telemetry/KPI
This feature turns raw event history into measurable policy evidence: what happened vs. what would have happened under alternate decisions.
That is fundamentally KPI instrumentation for decision quality, latency, and risk outcomes.

## Problem
We currently tune approval/review policy mostly by intuition. We need hard evidence for policy trade-offs (speed vs safety).

## Proposed mechanism
- Replay historical decision points with alternate choices (approve/defer/escalate/reject).
- Compare observed outcomes to simulated outcomes.
- Emit KPI deltas by policy variant.

## Example outputs
- Latency deltas (p50/p90) by priority lane.
- Estimated failure/risk exposure delta.
- “Top 3 policy shifts” with projected gain and caveat.

## Earliest prototype
- Artifact: `analysis/counterfactual_replayer.py`
- Input: normalized decision event log export.
- Output: markdown + JSON report (`artifacts/counterfactual-report.*`).

## Initial success thresholds
- Identify >=2 policy changes with projected latency improvement >=15% and no increase in high-risk failure rate.

## Risks
- Simulation fidelity may be weak if event logs are incomplete.
- Counterfactual assumptions could overstate gains; must label confidence bands.

## Notes
- This should stay enhancement-scoped until core RelayTrace control-plane primitives are stable.
