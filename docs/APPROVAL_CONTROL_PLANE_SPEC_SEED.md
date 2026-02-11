# Approval Control Plane (ACP) — Spec Seed

Date: 2026-02-08
Owner: Redact + Wit
Status: Draft seed for feasibility + architecture research

## Intent
Build a platform that acts as the **supervisor layer** for autonomous agents and human approvers.

Working metaphor: **NASA Mission Control**
- Operator desks monitor active workflows
- Escalation paths route decisions to higher-authority desks
- Bi-directional communication with agents for clarification and constrained approvals

## Constraints / Preferences (locked for now)
1. **Self-hosted** first
2. **Persistent/durable containers** for runtime services
3. **Open-source** streaming/queueing stack
4. Start **small-scale prototype**, but design for growth
5. Human + agent registration and queue/workload ownership model
6. Platform is a **supervisor**, not just a passive workflow inbox
7. Focus on **business workflow approvals** (not CI/dev workflow approvals)
8. Integration model should be a **base library + wrapper/decorator** usable across agent frameworks (example target: AWS Strands wrapper/decorator extension)

## Product Thesis
A common interface for humans to supervise autonomous agents:
- route approvals
- visualize system state and pending decisions
- ask questions before decision
- return structured decisions to agents
- enforce escalation and policy

## Core Capability Blocks
1. **Event Ingest API** for agent approval requests
2. **Routing + policy engine** (role/risk/time/SLA aware)
3. **Supervisor console** (queues, statuses, escalation ladders)
4. **Clarification loop** (human ↔ agent Q&A)
5. **Decision callback contract** (approve/reject/needs-info/approve-with-constraints)
6. **Audit trail** + metrics (latency, bottlenecks, exceptions)

## Feasibility Study Goals (P0)
1. Determine if this is already solved by an existing platform
2. Identify where incumbents stop short (agent-native supervision gap)
3. Validate enterprise pain and buyer urgency in **business operations workflows**
4. Evaluate buy-vs-build economics
5. Recommend MVP scope + architecture path
6. Define a realistic **low-token / low-cost experimentation path** for initial internal pilots

## Research Questions
### Market / Competitive
- Which products already handle approval routing + escalation + audit?
- Which products are explicitly **agent-native** vs generic workflow tools?
- What do enterprises use today (ServiceNow/Jira/Slack/email/custom)?

### Enterprise Adoption
- Who owns budget and rollout (security, platform eng, IT ops, compliance)?
- In regulated orgs, what controls are mandatory for adoption?
- Why would they buy vs build this in-house?

### Technical
- What queue/stream stack best fits self-hosted and gradual scale?
- What durability model is needed for decision/event history?
- What latency/SLA targets matter for human approvals?

### Product
- What is the smallest “Mission Control” UX that proves value?
- What context card shape maximizes approval quality?
- What escalation policies are needed in v1 vs later?

## Candidate OSS Architecture (to test, not final)
- API: FastAPI
- Queue/Stream: NATS JetStream or Redis Streams (evaluate both)
- Durable DB: Postgres
- Realtime fanout: WebSocket/SSE gateway
- Policy engine: OPA (optional in phase 1; simple rules first)
- Worker runtime: containerized Python workers
- UI: React + server-pushed updates

## Success Criteria for P0
- Clear competitor map with “build vs buy” recommendation
- 2–3 enterprise personas with likely buying path
- Risk register (technical + GTM)
- MVP definition for 60–90 day prototype
- Decision memo: proceed / narrow / pause

## Product Direction Decisions (from Redact, 2026-02-08)
1. **Customer focus (initial):** mixed enterprise stakeholders (security/compliance + platform + IT/ops), centered on business workflows rather than developer CI loops.
2. **MVP domain:** business approvals with high-ambiguity edge cases, e.g.:
   - Security triage escalation (50/50 threat/noise cases)
   - Healthcare adjudication escalation (missing/conflicting data, flagged conditions)
3. **Wedge strategy:** start as **Approval Control Plane for Agents**, expand toward **Mission Control for Agent Operations**.
4. **Integration strategy:** provide a reusable SDK/wrapper/decorator that can sit on top of framework-native agent decorators/prompts/tooling.

## Token-Light Work Plan (today)
1. Finalize this seed doc and assumptions
2. Build a local-first research template + scoring rubric
3. Queue external market scan for tomorrow when token budget resets

## Deliverables
- `docs/APPROVAL_CONTROL_PLANE_SPEC_SEED.md` (this file)
- Follow-up: `docs/APPROVAL_CONTROL_PLANE_FEASIBILITY.md` (market + recommendation)
- Follow-up: `docs/APPROVAL_CONTROL_PLANE_ARCH_OPTIONS.md` (architecture tradeoffs)
