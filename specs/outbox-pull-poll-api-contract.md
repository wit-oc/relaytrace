# Outbox Pull/Poll API Contract (MVP Stub)

## Goal
Define a deterministic pull/poll interface for agents and supervisor workers to retrieve pending items from RelayTrace-managed outboxes.

This contract is intentionally transport-agnostic and aligns with at-least-once delivery.

## Resource model
- **Outbox**: named queue-like logical stream (`agent-decisions`, `supervisor-requests`, etc.)
- **Cursor token**: opaque server-issued checkpoint
- **Lease**: short visibility timeout during processing

## Endpoints (v1)

### 1) Pull batch
`POST /v1/outbox/{outbox_name}/pull`

Request:
```json
{
  "consumer_id": "agent:sec-triage-01",
  "max_items": 25,
  "wait_ms": 15000,
  "cursor": "opaque-cursor-token-optional"
}
```

Response:
```json
{
  "outbox": "agent-decisions",
  "consumer_id": "agent:sec-triage-01",
  "items": [
    {
      "message_id": "msg_01J...",
      "request_id": "req_01J...",
      "event_type": "handoff.decided",
      "event_version": 1,
      "occurred_at": "2026-02-13T23:30:00Z",
      "payload": {},
      "delivery": {
        "attempt": 1,
        "lease_expires_at": "2026-02-13T23:31:00Z"
      }
    }
  ],
  "next_cursor": "opaque-next-cursor",
  "server_time": "2026-02-13T23:30:05Z"
}
```

Behavior:
- Returns empty `items` when no messages within `wait_ms` long-poll window.
- Server grants per-message lease; unacked items may be redelivered after expiration.

### 2) Ack processed item(s)
`POST /v1/outbox/{outbox_name}/ack`

Request:
```json
{
  "consumer_id": "agent:sec-triage-01",
  "acks": [
    {
      "message_id": "msg_01J...",
      "status": "processed",
      "processed_at": "2026-02-13T23:30:11Z"
    }
  ]
}
```

Response:
```json
{
  "accepted": ["msg_01J..."],
  "rejected": []
}
```

### 3) Nack / retry item(s)
`POST /v1/outbox/{outbox_name}/nack`

Request:
```json
{
  "consumer_id": "agent:sec-triage-01",
  "nacks": [
    {
      "message_id": "msg_01J...",
      "reason": "checkpoint_load_failed",
      "retry_after_ms": 5000
    }
  ]
}
```

Response:
```json
{
  "accepted": ["msg_01J..."],
  "rejected": []
}
```

## Error model (stub)
- `400` invalid payload
- `401/403` authn/authz failure
- `404` outbox not found
- `409` stale/invalid lease or duplicate terminal ack
- `429` pull rate limited
- `500` internal failure

Error envelope:
```json
{
  "error": {
    "code": "STALE_LEASE",
    "message": "Lease expired for message msg_...",
    "retryable": true
  }
}
```

## Idempotency and ordering
- Ack/Nack operations are idempotent per `(outbox, consumer_id, message_id)`.
- Delivery is at-least-once; consumers must dedupe by `message_id` and domain key (`request_id`).
- Ordering is best-effort within an outbox partition lane; strict global ordering is not guaranteed.

## Auth stub
- Bearer token for MVP.
- Token must map to allowed `consumer_id` prefixes.

## OpenAPI stub (minimal)
```yaml
openapi: 3.1.0
info:
  title: RelayTrace Outbox Pull/Poll API
  version: 0.1.0
paths:
  /v1/outbox/{outbox_name}/pull:
    post:
      summary: Pull a batch from outbox
  /v1/outbox/{outbox_name}/ack:
    post:
      summary: Ack processed items
  /v1/outbox/{outbox_name}/nack:
    post:
      summary: Nack and requeue items
```

## Implementation stub target
Initial no-op handler should:
- validate request shape
- return deterministic empty pull response with `next_cursor`
- accept ack/nack payloads and return `accepted=[]` until persistence layer lands
