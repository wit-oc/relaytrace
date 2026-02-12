# RelayTrace MVP Auth, Reliability, and Ops Spec

## 1) Agent/Auth Model
- Per-agent identity and key relationship.
- Signed token authentication for agent->RelayTrace.
- Key rotation policy:
  - rotate at ~75% key lifetime,
  - support overlapping valid keys,
  - agent prefers newest key.

## 2) Decision Authenticity Verification (Agent-Side)
Agent must verify:
- HMAC signature over canonical payload.
- Timestamp freshness window.
- Nonce/JTI anti-replay.
- Issuer + key_id validity.
- `request_id` correlation.

## 3) Reliability Semantics
- Delivery: at-least-once.
- Handler behavior: idempotent by `request_id`/dedupe strategy.
- No silent failure paths.

Retry matrix (MVP baseline):
1. Transient transport/infra error -> retry with backoff.
2. Pending HITL timeout -> explicit timeout/failure outcome.
3. Contract-invalid payload -> no retry; route to dead-letter/error queue.

## 4) Dedupe + Retention
- Dedupe retention window: 7 days.
- Optional fast-path cache window (e.g., 24h) for performance.

## 5) Fault/Recovery
- Agent fault: resume via checkpoint + tail events.
- Platform fault: rely on durable queue + Postgres persistence first.
- Event log remains audit source of truth.
- Replay/backfill: admin-only in MVP.

## 6) Observability + Operations
- Logs-first observability for MVP.
- Core operational counters:
  - HITL request count
  - Approval ratio
- Additional metrics/traces deferred.

## 7) Security/Authorization Notes
- Supervisor identity includes tenant/principal/role/scope and source IP.
- Reroute disabled in MVP.
- Agent cancel of pending HITL disabled in MVP.
- Decisions immutable after submit.
