# AWS AgentCore + Strands Adapter Spec (RelayTrace v0.1)

## Objective
Provide a reference adapter that extends Strands-based agents with RelayTrace supervisory capabilities:
- HITL event raising
- approval/handoff payload packaging
- callback handling for operator decisions
- checkpoint-aware resume semantics

---

## 1) Adapter Design Goals
1. **Minimal agent intrusion**: decorator/wrapper pattern around existing Strands agents
2. **Deterministic event contract**: predictable JSON payloads for request/decision
3. **Checkpoint-safe resumption**: agent can continue from pre-handoff state
4. **Policy-driven triggers**: emit HITL only when conditions require it
5. **Auditable by default**: all requests/decisions get trace IDs and receipts

---

## 2) Integration Surface

### 2.1 Wrapper/Decorator API (proposed)
```python
@relaytrace_supervised(
  agent_id="sec-triage-01",
  supervisors=["sec-oncall", "sec-lead"],
  policy_profile="default-security"
)
def run_agent(task_input):
    ...
```

### 2.2 Runtime hooks
- `before_action(action_ctx)`
- `after_action(result_ctx)`
- `on_risk_threshold(trigger_ctx)` -> emit handoff
- `on_decision(decision_ctx)` -> resume/alter execution

### 2.3 Required adapter config
- `relaytrace_endpoint` (API/stream gateway)
- `agent_id`
- `supervisor_roles[]`
- `routing_policy_id`
- `callback_channel` / subscription subject
- `checkpoint_strategy` (inline|external-ref)

---

## 3) HITL Trigger Conditions

Adapter should emit handoff when one or more conditions are met:
- low confidence + high impact action
- policy violation risk
- ambiguous classification near threshold (e.g., 50/50 risk)
- missing required evidence for irreversible action
- explicit agent rule: "human approval required"

Trigger output:
- `trigger_reason`
- `policy_rule_id`
- `confidence_score`
- `risk_level`

---

## 4) Request Payload (Agent -> RelayTrace)

```json
{
  "event_type": "handoff.requested",
  "request_id": "uuid",
  "trace_id": "uuid",
  "agent": {
    "agent_id": "string",
    "sdk": "aws-strands",
    "version": "string"
  },
  "workflow": {
    "workflow_id": "string",
    "run_id": "string",
    "step_id": "string"
  },
  "routing": {
    "supervisors": ["role_or_user_id"],
    "routing_policy_id": "string",
    "priority": "low|medium|high|critical"
  },
  "intent": {
    "summary": "string",
    "proposed_action": "string",
    "risk_level": "low|medium|high|critical",
    "confidence": 0.0
  },
  "checkpoint": {
    "mode": "external_ref",
    "ref": "s3://... or db://...",
    "state_hash": "sha256"
  },
  "context": {
    "messages": [],
    "artifacts": [],
    "citations": [],
    "required_by_ts": "ISO-8601"
  }
}
```

---

## 5) Decision Payload (RelayTrace -> Agent)

```json
{
  "event_type": "handoff.decided",
  "request_id": "uuid",
  "trace_id": "uuid",
  "decision": {
    "status": "approved|rejected|rerouted|needs_info",
    "operator_id": "string",
    "operator_role": "string",
    "context": "optional additional guidance",
    "constraints": ["optional machine-readable constraints"]
  },
  "decision_ts": "ISO-8601"
}
```

Adapter responsibilities on receipt:
- validate request/trace correlation
- load checkpoint
- append operator context to controlled system/developer context channel
- execute continuation policy for decision status
- emit `audit.receipt`

---

## 6) Continuation Policy (agent-owned)

The adapter supplies a default mapping, overridable per agent:
- `approved` -> continue next action
- `rejected` -> halt and raise terminal status (or rollback subroutine)
- `rerouted` -> continue waiting for final decision
- `needs_info` -> gather requested evidence and re-submit handoff

### 6.1 Non-blocking decision lanes (required)
HITL requests must be lane-scoped so agents can continue unrelated work.

Example: if an agent processes 100+ events/hour and ~1% require HITL, only those flagged items should pause. Other events continue through non-blocked lanes.

Required mechanics:
- `lane_id` on each task/event unit
- checkpoint state per lane (not global-run freeze)
- concurrency-safe pause/resume by `lane_id`
- bounded in-flight HITL queue per lane to avoid backpressure collapse
- optional per-lane timeout policy (`auto-expire`, `reroute`, or `fallback action`)

---

## 7) Prompt/Definition Enrichment Strategy

The wrapper should inject RelayTrace operational context into agent definitions:
- what HITL means for this agent
- when to trigger handoff
- what context quality is required in handoff payload
- how to behave on approve/reject/reroute/needs_info

Guardrail: keep injected guidance procedural and bounded; avoid exposing private operator metadata to unrelated runs.

---

## 8) Reliability Requirements
- at-least-once event delivery with idempotent processing
- deterministic `request_id` generation option
- replay-safe decision handling
- timeout + escalation if no decision before SLA
- dead-letter queue for malformed payloads

---

## 9) Security Requirements
- signed event payloads (or mTLS channel)
- scoped credentials per agent identity
- policy enforcement before emitting high-risk action requests
- redact sensitive fields in operator-facing payload unless authorized

---

## 10) Metrics and telemetry (future-state plan, begin in v1)

RelayTrace should emit telemetry events for both runtime and improvement loops.

### 10.1 Core HITL quality metrics
- `% events requiring HITL` = `handoff.requested / total actionable events`
- `% approvals` / `% rejections` / `% reroutes` / `% needs_info`
- decision latency (P50/P95)
- escalation rate
- queue depth and stale-request count

### 10.2 Model quality proxy metrics
- false-positive proxy: high `% rejected` on similar trigger classes
- false-negative proxy: post-incident/manual findings where HITL should have been raised but was not
- retry/rework rate after `needs_info`

### 10.3 Persona-separated dashboards
- **Operator dashboard:** active queues, urgency, decisions, SLA risk
- **Engineering dashboard:** trigger quality, HITL ratios, policy drift, model/workflow tuning signals

This separation is required because HITL responders and agent engineers are often different teams.

---

## 11) MVP Implementation Plan
1. Python wrapper/decorator package (`relaytrace-strands-adapter`)
2. Event emitter client (request + audit)
3. Decision listener client (poll/subscription)
4. Checkpoint helper contract (S3/ref-based) with lane-scoped pause/resume
5. Metrics emitter for HITL + decision outcomes
6. Minimal example in `examples/agentcore-wrapper-minimal`

---

## 12) Open Questions
- Should request UUID originate at agent or RelayTrace ingress?
- Push callbacks vs pull/poll for decision retrieval in constrained networks?
- Should `rerouted` be terminal to origin agent or transitional state only?
- How much checkpoint state is embedded vs externally referenced?
- Which telemetry schema is canonical for cross-team analytics (OTel attrs vs domain-specific event model)?
