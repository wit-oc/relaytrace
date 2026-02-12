# RelayTrace MVP Event + API Contract Spec

## 1) Canonical Event Envelope
Required fields:
- `event_type` (string)
- `event_version` (integer, start at 1)
- `event_id` (global unique id)
- `request_id` (correlation id)
- `occurred_at` (UTC ISO-8601)
- `source` (agent/service origin)
- `payload` (object)

Compatibility rules:
- Additive changes allowed within major version.
- Breaking changes require versioned migration and deprecation runway.

## 2) Event Types
### `handoff.requested`
Required payload fields:
- `request_id`
- `from_agent`
- `intent`
- `context_ref` (or minimal inline context)
- `occurred_at`

Optional payload fields:
- `priority`
- `deadline_at`
- `constraints`
- `metadata`

### `handoff.decided`
Required payload fields:
- `request_id`
- `decision_id`
- `final_status` (`approved|rejected|deferred`)
- `approvers`
- `decision_reason` (free-form text)
- `decided_at`

Optional payload fields:
- `target_agent`
- `execution_window`
- `metadata`

## 3) Request ID Ownership
- Agent submits `client_request_key` (idempotency/correlation candidate).
- RelayTrace validates input + canonicalizes authoritative `request_id`.
- System stores both values for traceability.

## 4) API Versioning
- URI versioning for MVP (`/v1/...`).
- Version bump only for breaking contract changes.

## 5) Candidate Endpoint Set (MVP)
- `POST /v1/agents/register` (manual-admin mediated flow)
- `POST /v1/hitl/requests`
- `GET /v1/hitl/requests/{request_id}`
- `POST /v1/hitl/decisions/{request_id}`
- `GET /v1/agents/{agent_id}/decisions/poll`

## 6) Decision Chain Model
Persist append-only `approval_chain[]` entries:
- `actor_id`
- `action`
- `timestamp`
- `reason`
- `from_assignee` (optional)
- `to_assignee` (optional)
- `proof_ref` (optional, future)
