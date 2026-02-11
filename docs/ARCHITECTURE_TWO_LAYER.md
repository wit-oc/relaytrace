# RelayTrace Two-Layer Architecture (AWS AgentCore + Strands)

## Purpose
Define the boundary between:
1) **Execution substrate** (AWS AgentCore + Strands agents)
2) **Supervisory control plane** (RelayTrace)

RelayTrace does not replace agent execution. It governs handoffs, approvals, routing, escalation, observability, and auditability.

---

## Layer 1 — Agent Execution Substrate (AWS AgentCore + Strands)

### Responsibilities
- Execute autonomous workflows
- Manage local tool calls and reasoning loop
- Detect HITL-required conditions
- Emit approval/handoff requests to RelayTrace
- Pause/resume task execution based on supervisory decision

### Components
- Strands agent SDK integration
- Agent tool/skill pack (domain-specific)
- Runtime checkpoint state
- Adapter client for RelayTrace events

### Output to RelayTrace
When policy/logic triggers HITL:
- create `handoff.requested` event
- include workflow state snapshot
- include action intent + risk metadata
- include candidate supervisors and routing hints

---

## Layer 2 — RelayTrace Supervisory Control Plane

### Responsibilities
- Ingest handoff/approval events from agents
- Route to correct operator queue/desk
- Support operator actions: **Approve / Reject / Reroute / Add Context**
- Enforce escalation and SLA policy
- Return structured decision payload to originating agent
- Maintain immutable audit trail and operator observability

### Components
- Ingest API / stream consumers
- Routing + escalation engine
- Operator queue + decision UI (Mission Control view)
- Decision callback API/pubsub
- Audit/event ledger + trace indexes

---

## End-to-End Flow (Happy path)
1. Strands agent reaches condition requiring HITL.
2. Agent adapter emits `handoff.requested` to RelayTrace stream/topic.
3. RelayTrace creates request UUID, resolves operator desk, and posts to queue.
4. Operator reviews full context and chooses action.
5. RelayTrace emits `handoff.decided` back to agent callback channel.
6. Agent resumes from checkpoint with decision + optional operator context.

---

## Operator Actions (v1 semantics)
- **Approve**: continue action path
- **Reject**: stop/rollback/escalate per agent policy
- **Reroute**: transfer request to another operator/role queue
- **Add Context**: attach additional instructions/facts for agent continuation

> Note: RelayTrace returns the decision envelope; each agent defines concrete continuation behavior.

---

## Data Contract Boundary

### Agent -> RelayTrace (request)
- `request_id` (agent-generated or assigned by RelayTrace)
- `agent_id`, `workflow_id`, `run_id`
- `task_checkpoint_ref` (or embedded checkpoint snapshot)
- `event_type` (`handoff.requested`)
- `intent_summary`
- `risk_level`, `confidence`
- `required_by_ts`
- `candidate_supervisors[]`
- `context_bundle` (artifacts, citations, prior decisions)

### RelayTrace -> Agent (decision)
- `request_id`
- `decision` (`approved|rejected|rerouted|needs_info`)
- `operator_id` / `operator_role`
- `decision_context` (freeform + structured fields)
- `decision_ts`
- `trace_id`

---

## Topic/Queue Pattern (initial recommendation)
- Event bus: topic-based stream (NATS JetStream or Kafka-compatible option)
- Per-role queue subscriptions for operator routing
- Durable retention on request/decision topics
- Idempotency key: `request_id + event_version`

Suggested subjects/topics:
- `relaytrace.handoff.requested`
- `relaytrace.handoff.decided`
- `relaytrace.handoff.escalated`
- `relaytrace.audit.append`

---

## Mission Control Visibility Model
- **Operator scope**: only requests assigned to their role/team/policy scope
- **Platform owner scope**: ecosystem-wide control-plane metadata and event health
- **Data minimization**: redact or link out sensitive payload sections when required

---

## Non-goals (v1)
- Replacing Strands/AgentCore runtime internals
- Defining business-domain decision policy for every customer
- Full workflow orchestration replacement for existing BPM systems
