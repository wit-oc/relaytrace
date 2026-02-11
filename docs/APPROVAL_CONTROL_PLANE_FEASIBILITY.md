# Approval Control Plane — Feasibility + Market Scan (Draft)

Date: 2026-02-10
Owner: Wit
Status: In progress (initial draft)

## Objective
Determine whether a self-hosted, agent-native approval control plane is a viable product opportunity, and where incumbents/adjacent tools already cover the space.

## Scope (aligned to Redact direction)
- Business workflow approvals first (not CI/developer-only workflows)
- Agent-native supervision model (human clarifications + structured decision return)
- Self-hosted, durable containers, open-source queue/stream core

## Core hypothesis
Most incumbents solve generic workflow approvals or process orchestration, but few deliver a dedicated agent-native control plane with:
1) policy-based routing/escalation,
2) bi-directional human↔agent clarification loop,
3) structured decision callbacks to autonomous workers,
4) mission-control style observability for multi-agent operations.

## Competitor map (working set)

### A) Workflow/approval incumbents
- ServiceNow
- Jira Service Management (Atlassian)
- Microsoft Power Automate / Logic Apps
- Salesforce Flow/Approvals

### B) Process/orchestration platforms
- Camunda
- Temporal
- UiPath
- Automation Anywhere

### C) Agent frameworks / agent ops / eval-adjacent
- LangGraph / LangChain HITL patterns
- Microsoft AutoGen / Semantic Kernel patterns
- Humanloop / LangSmith / TruLens / Arize-adjacent governance/observability tools

## Scoring dimensions (for each candidate)
1. Approval routing depth (roles, policy, quorum)
2. Escalation/SLA support
3. Human↔agent clarification loop
4. Structured decision return contract
5. Self-hosted maturity
6. Audit/compliance depth
7. Evidence of enterprise scale
8. Agent-native positioning (explicit vs incidental)

## Preliminary whitespace signal (unverified draft)
Potential gap appears strongest at the intersection of:
- strict enterprise governance + audit,
- self-hosted deployment,
- explicit agent-native supervision loop,
- and mission-control operations UX.

## Buy vs build lens (initial)
Why enterprises might still buy:
- policy/routing complexity grows quickly across teams and risk tiers
- auditability + escalation correctness becomes expensive to maintain in-house
- standardized agent integration contract reduces per-agent custom glue
- cross-workflow observability is often missing in piecemeal internal builds

Why enterprises might build instead:
- already pay for incumbent workflow stack
- strict internal architecture/security standards
- lower perceived need before agent operations reach critical scale

## Architecture feasibility frame (self-hosted first)
Candidate baseline stack for prototype:
- API: FastAPI
- Durable state: Postgres
- Queue/stream: NATS JetStream or Redis Streams (evaluate tradeoffs)
- Realtime events: WebSocket/SSE gateway
- Workers: containerized Python
- Policy: start simple rules; optional OPA phase-in

## Competitor matrix (preliminary, evidence-tiered)

### Tier 1 — Incumbent enterprise workflow suites (very large scale)
- ServiceNow
  - Relevance: strong approvals/routing/escalation in enterprise operations.
  - Gap vs ACP: not purpose-built as an agent-native supervision contract for autonomous agents.
  - Scale signal: global Fortune-1000 penetration and broad ITSM footprint.
- Atlassian (Jira Service Management + workflow stack)
  - Relevance: strong workflow control and team-level approvals.
  - Gap vs ACP: agent clarification loop + structured callback to autonomous agents is not core product identity.
  - Scale signal: very large global customer base across software/IT teams.
- Microsoft Power Platform / Logic Apps
  - Relevance: deeply embedded enterprise automation and approvals in Microsoft ecosystems.
  - Gap vs ACP: agent-native supervision model is possible but not opinionated as a dedicated control plane.
  - Scale signal: very high enterprise penetration where M365/Azure is standard.
- Salesforce Flow/Approvals
  - Relevance: business-process approvals with strong CRM-centric integration.
  - Gap vs ACP: not centered on cross-agent mission-control and autonomous worker callback contracts.
  - Scale signal: very large enterprise and mid-market footprint.

### Tier 2 — Process/orchestration and RPA platforms (large scale)
- UiPath / Automation Anywhere
  - Relevance: enterprise automation with human-in-the-loop checkpoints.
  - Gap vs ACP: historically bot/RPA-centric; agent-native governance is evolving but not standardized around multi-agent supervision desks.
  - Scale signal: large enterprise deployment base and mature partner ecosystems.
- Camunda
  - Relevance: robust process orchestration and human task modeling.
  - Gap vs ACP: provides primitives, but mission-control UX and agent-specific approval contract are typically custom-built.
  - Scale signal: significant enterprise adoption in process-heavy organizations.
- Temporal
  - Relevance: high-reliability workflow orchestration primitives.
  - Gap vs ACP: developer platform, not out-of-box enterprise approval control-plane UX/policy product.
  - Scale signal: widely adopted in modern engineering orgs for critical workflows.

### Tier 3 — Agent frameworks / observability ecosystems (emerging-to-growing)
- LangGraph/LangChain, AutoGen, Semantic Kernel patterns
  - Relevance: explicit agent construction + optional human-in-the-loop patterns.
  - Gap vs ACP: no single enterprise-grade, self-hosted approval routing + escalation + mission-control product standard across frameworks.
  - Scale signal: rapid adoption among AI engineering teams; enterprise standardization still fragmented.
- Observability/eval tools (e.g., LangSmith/Humanloop/TruLens/Arize-adjacent)
  - Relevance: quality/trace/eval layers around LLM systems.
  - Gap vs ACP: typically monitor/evaluate rather than own real-time decision routing/escalation as a supervisor control plane.
  - Scale signal: growing in production AI stacks, especially in experimentation-to-production transitions.

## Synthesis: what appears crowded vs open
Crowded:
- Generic approvals
- BPM/workflow orchestration
- RPA with human checkpoints

Open / weaker coverage:
- Agent-native, framework-agnostic approval contract
- Bi-directional clarification loop with structured decision return to autonomous workers
- Mission-control operations UX for multi-agent supervision with escalation ladders
- Self-hosted-first packaging tuned for governance-heavy enterprises

## Strategic feedback (proceed / narrow / pause)
Recommendation: **Proceed, but narrow aggressively.**

Narrow to this wedge:
- "Approval Control Plane for autonomous business workflows" with two initial domains:
  1) Security triage edge-case escalation
  2) Regulated adjudication/exception handling (healthcare/claims-style)

Why this wedge can beat buy-vs-build:
- internal builds usually handle routing, but underinvest in policy quality, escalation correctness, and cross-agent observability.
- if we package those as defaults (with audit receipts and self-hosted operability), we reduce operational burden enough to justify adoption.

## Next deliverables
1) Source-verified matrix with explicit citations + confidence tags (High/Med/Low)
2) Top-3 wedge options + recommended entry wedge
3) 60–90 day MVP definition
4) Risk register and de-risk plan

## Notes
- This file is intentionally token-light and serves as a durable checkpoint.
- This draft is a **preliminary market pass**; numbers/claims should be citation-hardened before external use.
- Source of truth for product intent: `docs/APPROVAL_CONTROL_PLANE_SPEC_SEED.md`.
