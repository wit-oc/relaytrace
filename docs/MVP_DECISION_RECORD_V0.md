# RelayTrace MVP — Decision Record v0

Date: 2026-02-11  
Status: Locked (Q&A synthesis, 51/51)

## 1) MVP Success Criteria (Definition of Done)
1. Agents can register with the platform (manual admin onboarding).
2. Agent definition can express conditions that trigger HITL requests.
3. Platform records and logs HITL events and decisions.
4. HITL events are surfaced to authenticated operators for disposition.
5. Agents can retrieve decision records via pull/queue polling flow.

## 2) Core Contract Decisions
- Canonical event envelope includes: `event_type`, `event_version`, `event_id`, `request_id`, `occurred_at`, `source`, `payload`.
- Non-breaking evolution default; breaking changes require multi-version migration/deprecation path.
- `request_id` is canonicalized by RelayTrace ingress; client-side key may be retained as reference.
- `handoff.requested` and `handoff.decided` remain lean envelopes with contextual expansion in payload/refs.

## 3) Delivery + Reliability
- Delivery posture: push-first for ingress; agent polling for decision retrieval in MVP.
- Reliability: at-least-once + idempotent handlers.
- Retry behavior exists; no silent failures.
- HITL unresolved in allowed window: explicit failure/timeout path; agent retry/orchestrator logic handles re-attempt.
- Default timeout windows by priority:
  - P1: 1 hour
  - P2: 24 hours
  - P3: 14 days
- Timeout disposition default: auto-reject (configurable globally, override by agent).

## 4) Checkpoint/Replay
- Resume context for MVP is present in payload (rich enough for immediate agent disposition).
- Checkpoint strategy: step-level persisted checkpoints; action-level audit/gating events.
- Replay model: event log remains source of truth; operational recovery uses checkpoint + tail replay.
- Replay/backfill in MVP is admin-triggered/internal only.

## 5) Identity, Auth, and Trust
- Supervisor decision identity includes tenant/principal/role/scope context and source IP.
- Agent/backend trust path uses signed tokens with per-agent key relationship.
- Rotation policy: rotate at ~75% key lifetime, support overlap, prefer newest key.
- Decision authenticity verification (MVP): HMAC-signed envelope + timestamp freshness + nonce/jti + key_id + strict issuer/correlation checks.

## 6) Authorization + Custody
- Reroute is disabled in MVP UI.
- Long-term reroute is delegation transfer with preserved custody chain.
- Audit/custody model is append-only approval chain (`approval_chain[]`), immutable prior entries.
- No post-submit decision edit in MVP (agent-side remediation if needed).

## 7) Data + Storage + Messaging
- Primary persistence: Postgres.
- Dedupe retention baseline: 7 days (with optional short hot-path optimization).
- Queueing for local/container MVP: NATS JetStream.

## 8) Product Scope and Non-Goals
### In Scope
- Operator-first workflow value.
- Function-over-form UI.
- Rules-based policy guardrails.

### Explicit Non-Goals (MVP)
- Advanced policy DSL.
- Dual-approval requirements.
- Partial approvals/conditional approvals.
- Operator self-serve replay tooling.
- Reroute workflow.
- SLA breach notifications.
- Identity federation/SSO.

## 9) Ops and Observability
- Metrics kept minimal in MVP; logs-first observability posture.
- Core operational metrics include HITL count and approval ratio (expand over time).
- Data retention is config-driven; default 30 days for MVP.
- No delete path for audit/event records.

## 10) Pilot Plan (Initial)
- Internal-only pilot/mock implementation.
- Goal is to validate real need and workflow fit before broader rollout.
- Primary technical risks to track:
  1. Autonomous agent integration reliability.
  2. Data stream/flow correctness under load and retries.
  3. Team maturity with autonomous-agent operational patterns.

## 11) Open Questions (Post-MVP / Design Refinement)
1. Programmatic onboarding/offboarding API shape.
2. Multi-tenant hosted model specifics (including account/env isolation strategy).
3. Future reroute authorization model and guardrails.
4. Long-term observability stack (metrics/traces) and optional external telemetry joins.
5. Capability model richness in agent identity records.
