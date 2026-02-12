# RelayTrace MVP System Spec

Status: Draft from Decision Record v0

## Goal
Deliver a self-hosted, operator-first HITL control plane for autonomous agents with durable auditability and reliable decision return flow.

## Architecture (MVP)
- API: single deployable backend with stable URI contracts (`/v1/...`).
- Storage: Postgres (events, decisions, approvals, agent identities).
- Queue: NATS JetStream for request/decision messaging.
- UI: operator queue + decision actions (approve/reject).
- Auth: signed token model with per-agent keying.

## End-to-End Runtime
1. Agent submits HITL request (`handoff.requested`).
2. RelayTrace validates/canonicalizes IDs and persists event.
3. Request appears in operator queue.
4. Operator decides (approve/reject + free-form reason).
5. RelayTrace persists `handoff.decided` + decision chain entry.
6. Agent polling consumer retrieves decision from dedicated queue/endpoint.
7. Agent dispositions workflow and continues/halts.

## MVP UI Features
- List pending HITL items.
- View request context.
- Single-item approve/reject actions only.
- No reroute.
- No post-submit edit.

## Priority + Timeout Policy
- P1: 1h
- P2: 24h
- P3: 14d
- Default timeout disposition: auto-reject (configurable global + per-agent override).

## Data Retention + Mutability
- Audit/event records are append-only.
- No delete path in MVP.
- Retention configurable; default 30 days.

## Non-Goals
- SSO/federation.
- Advanced policy DSL.
- Partial approvals.
- Batch approvals.
- SLA notifications.
- Tenant policy admin UI.
