# Approval Event Contract (Draft)

## Event: `approval.requested`

```json
{
  "event_type": "approval.requested",
  "request_id": "uuid",
  "agent_id": "string",
  "workflow_id": "string",
  "risk_level": "low|medium|high|critical",
  "action_summary": "string",
  "resource_scope": "string",
  "deadline": "ISO-8601",
  "rollback_plan": "string",
  "context": {
    "artifacts": ["uri"],
    "evidence": ["string"],
    "trace_id": "string"
  }
}
```
