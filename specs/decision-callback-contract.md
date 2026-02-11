# Decision Callback Contract (Draft)

## Event: `approval.decided`

```json
{
  "event_type": "approval.decided",
  "request_id": "uuid",
  "decision": "approved|rejected|needs_info|approved_with_constraints",
  "constraints": ["string"],
  "decision_rationale": "string",
  "decided_by": "user_or_role_id",
  "decided_at": "ISO-8601",
  "trace_id": "string"
}
```
