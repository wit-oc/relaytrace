# RelayTrace MVP Development Work Plan (Taskable)

## Phase 0 — Foundations
1. Define Postgres schema (agents, hitl_requests, hitl_decisions, approval_chain, dedupe index).
2. Stand up NATS JetStream in container stack.
3. Scaffold `/v1` API service and config system.
4. Add structured logging baseline.

## Phase 1 — Core Contracts + Ingest
1. Implement canonical envelope validation.
2. Implement `request_id` canonicalization + `client_request_key` retention.
3. Build `POST /v1/hitl/requests` ingest endpoint.
4. Persist request + enqueue operator-visible work item.
5. Implement dedupe checks (7-day retention policy).

## Phase 2 — Operator Decision Loop
1. Build operator queue list UI/API.
2. Build request detail + approve/reject action.
3. Implement decision persistence + append-only `approval_chain`.
4. Emit `handoff.decided` event.
5. Enforce no post-submit edits.

## Phase 3 — Agent Poll/Resume Path
1. Build `GET /v1/agents/{agent_id}/decisions/poll`.
2. Implement agent auth (signed tokens + key_id handling).
3. Implement response authenticity envelope (HMAC+timestamp+nonce).
4. Return decision payload with required fields and resume context.

## Phase 4 — Reliability + Controls
1. Implement retry/error classification for ingest + decision delivery.
2. Add DLQ/error queue behavior for non-retryable failures.
3. Implement timeout policy engine (P1/P2/P3 + auto-reject default).
4. Add admin controls for stale/disposition workflows.
5. Add admin-triggered replay/backfill endpoint (internal only).

## Phase 5 — Simulator + Internal Pilot
1. Build synthetic agent simulator:
   - submit requests,
   - poll/retry,
   - handle approve/reject.
2. Run baseline test scenarios and record outcomes.
3. Validate success criteria from Decision Record v0.
4. Produce pilot findings memo (fit, risks, recommended next iteration).

## Backlog (Post-MVP)
- Programmatic onboarding/offboarding APIs.
- Reroute workflow + delegated authority model.
- Advanced policy DSL.
- SSO/federation.
- Batch approvals.
- Metrics/traces and SLA notifications.
- Hosted multi-tenant architecture hardening.
