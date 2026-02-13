# AgentCore + Strands Adapter Decision Log (NOW vs LATER)

Date: 2026-02-13  
Scope: RelayTrace adapter implementation choices to reduce architecture churn for MVP.

## Decision Rules
- **NOW** = lock for MVP build and tests.
- **LATER** = explicitly deferred; document boundary so current implementation does not block future direction.

---

## 1) Adapter shape
- **NOW:** Python decorator/wrapper package (`relaytrace-strands-adapter`) around existing Strands agents.
- **LATER:** Additional language SDKs and deep framework-specific plugin variants.
- **Why:** Fastest path to validate supervision flow with minimal agent intrusion.

## 2) Event contracts
- **NOW:** Freeze `handoff.requested` and `handoff.decided` payload envelopes from `AWS_AGENTCORE_STRANDS_ADAPTER_SPEC.md` with required IDs (`request_id`, `trace_id`, `lane_id`).
- **LATER:** Add optional extension blocks for vertical-specific metadata.
- **Why:** Contract stability is prerequisite for UI, routing, and callback reliability.

## 3) Checkpoint strategy
- **NOW:** `checkpoint.mode=external_ref` only (S3/DB reference + state hash).
- **LATER:** Inline checkpoint payloads for very small state snapshots.
- **Why:** Keeps event size bounded and avoids transport/storage coupling.

## 4) Decision transport
- **NOW:** Pull/poll decision listener with idempotent cursor + retry backoff.
- **LATER:** Push callbacks/webhooks and bidirectional streaming.
- **Why:** Polling is easier to harden first in constrained enterprise networks.

## 5) Continuation semantics
- **NOW:** Implement explicit mapping for `approved|rejected|rerouted|needs_info` exactly as adapter policy defaults.
- **LATER:** Policy plugins with per-workflow custom transitions.
- **Why:** Deterministic defaults unblock implementation and operator training.

## 6) Concurrency model
- **NOW:** Lane-scoped pause/resume (`lane_id`) so HITL blocks only affected work units.
- **LATER:** Advanced global schedulers and adaptive lane rebalancing.
- **Why:** Prevents throughput collapse while keeping runtime logic understandable.

## 7) Reliability envelope
- **NOW:** At-least-once delivery, idempotent request/decision handling, replay-safe processing, timeout escalation, DLQ for malformed events.
- **LATER:** Exactly-once aspirations and cross-region active-active replay orchestration.
- **Why:** MVP reliability should be operable before optimizing for stricter guarantees.

## 8) Security baseline
- **NOW:** Signed payloads (or mTLS), scoped agent credentials, policy check before high-risk handoff, field-level redaction for operator view.
- **LATER:** Hardware-backed key management paths and tenant-specific crypto policies.
- **Why:** Minimum secure-by-default posture is required for approval workflows.

## 9) Telemetry
- **NOW:** Emit core HITL metrics (`handoff rate`, decision mix, latency p50/p95, stale queue count) with stable event names.
- **LATER:** Full persona dashboards and drift analytics automation.
- **Why:** Need immediate operability signals without over-building analytics stack.

## 10) Request ID ownership
- **NOW:** Agent generates deterministic `request_id` (configurable strategy) before emission.
- **LATER:** Optional ingress-side ID assignment for legacy clients.
- **Why:** Improves dedupe and trace continuity at the source.

## 11) Versioning & compatibility
- **NOW:** Add `contract_version` field and enforce backward-compatible additive changes in v0.x.
- **LATER:** Formal migration framework with schema registry.
- **Why:** Prevents accidental breaking changes while APIs are still settling.

## 12) MVP non-goals (explicitly deferred)
- Multi-language adapters
- Webhook signing key rotation automation
- Inline checkpoint compression/encryption strategy
- Fully automated policy tuning loop

---

## Implementation Guardrails
1. Do not add new decision statuses without updating both contract tests and continuation mapping.
2. Do not switch checkpoint mode from `external_ref` during MVP.
3. Do not introduce push callbacks until poller SLA and idempotency tests are green.
4. Any schema change must include fixture updates for request/decision golden files.

## Churn-avoidance outcome
This decision log intentionally locks the smallest viable architecture for MVP while preserving clear extension seams. Any deviation from a **NOW** decision requires a written delta in this file before code changes land.
