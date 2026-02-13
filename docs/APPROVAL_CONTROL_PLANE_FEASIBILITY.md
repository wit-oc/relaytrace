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

## Competitor matrix (source-hardened, citation-linked)

Confidence rubric:
- **High** = official docs + audited filing/investor reporting support the claim.
- **Med** = official docs support capability, but scale/adoption signal is marketing-grade or indirect.
- **Low** = directional signal only (none used below).

### Tier 1 — Incumbent enterprise workflow suites

- **ServiceNow** — **Confidence: High**
  - Relevance: enterprise workflow/approval and governance depth is strong.
  - Gap vs ACP: no default, framework-agnostic agent supervision contract (clarification loop + structured callback) as primary product surface.
  - Sources:
    - Workflow/approval capabilities: https://www.servicenow.com/products/enterprise-workflows.html
    - Scale/adoption signal (customer metrics in annual report / investor materials): https://investors.servicenow.com/

- **Atlassian (Jira Service Management + Jira Automation)** — **Confidence: High**
  - Relevance: mature team/service workflow approvals and automation primitives.
  - Gap vs ACP: agent-native mission-control UX and decision-callback contract are not central product abstractions.
  - Sources:
    - JSM approvals/workflows: https://support.atlassian.com/jira-service-management-cloud/docs/set-up-approvals/
    - Customer scale disclosure (annual report/investor): https://investors.atlassian.com/

- **Microsoft Power Automate / Logic Apps** — **Confidence: Med**
  - Relevance: broad enterprise automation with built-in approvals and connectors.
  - Gap vs ACP: supports HITL patterns, but not packaged as a dedicated autonomous-agent approval control plane.
  - Sources:
    - Power Automate approvals: https://learn.microsoft.com/power-automate/approvals-overview
    - Logic Apps workflow orchestration: https://learn.microsoft.com/azure/logic-apps/logic-apps-overview

- **Salesforce Flow / Approvals** — **Confidence: Med**
  - Relevance: strong business-process approvals within CRM-centric estates.
  - Gap vs ACP: cross-agent supervision + structured agent callback is not the core operating model.
  - Sources:
    - Salesforce approvals docs: https://help.salesforce.com/s/articleView?id=sf.approvals_overview.htm&type=5
    - Flow builder docs: https://help.salesforce.com/s/articleView?id=sf.flow.htm&type=5

### Tier 2 — Process orchestration + RPA

- **UiPath** — **Confidence: High**
  - Relevance: enterprise automation platform with human-in-the-loop checkpoints and governance tooling.
  - Gap vs ACP: historically automation/bot-first; agent-native, framework-agnostic supervision desk remains less opinionated.
  - Sources:
    - Product capability overview: https://www.uipath.com/product
    - Adoption/scale disclosures (investor): https://ir.uipath.com/

- **Camunda** — **Confidence: Med**
  - Relevance: robust BPMN/process orchestration + human tasks.
  - Gap vs ACP: strong primitives, but mission-control + agent-specific approval contract usually requires custom composition.
  - Sources:
    - Platform overview: https://camunda.com/platform/
    - Human task modeling/docs: https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/

- **Temporal** — **Confidence: Med**
  - Relevance: durable workflow orchestration for critical backend processes.
  - Gap vs ACP: developer orchestration platform, not packaged enterprise approval control plane with policy/escalation UX out-of-box.
  - Sources:
    - Platform docs: https://docs.temporal.io/
    - Core value proposition: https://temporal.io/

### Tier 3 — Agent frameworks / eval-adjacent tools

- **LangGraph / LangChain, AutoGen, Semantic Kernel** — **Confidence: Med**
  - Relevance: explicit agent-construction ecosystems with optional HITL checkpoints.
  - Gap vs ACP: no shared, enterprise-standard supervision contract spanning routing/escalation/audit + callback semantics.
  - Sources:
    - LangGraph docs: https://langchain-ai.github.io/langgraph/
    - AutoGen docs: https://microsoft.github.io/autogen/
    - Semantic Kernel docs: https://learn.microsoft.com/semantic-kernel/

- **LangSmith / Humanloop / TruLens / Arize Phoenix (observability/eval)** — **Confidence: Med**
  - Relevance: strong tracing, evaluation, quality feedback loops.
  - Gap vs ACP: typically monitor/evaluate; they do not generally own real-time approval routing/escalation as the supervisor control plane.
  - Sources:
    - LangSmith: https://docs.smith.langchain.com/
    - Humanloop: https://humanloop.com/
    - TruLens: https://www.trulens.org/
    - Arize Phoenix: https://phoenix.arize.com/

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

## Final recommendation (locked for execution)
Recommendation: **Proceed with a narrow, pull/poll-first MVP under the RelayTrace name.**

Locked decisions to preserve through implementation:
- Product name: **RelayTrace**
- Supervision mode: **pull/poll-first** (worker polls for decision state; push callbacks are optional later)
- SLA defaults:
  - **P1: 1 hour**
  - **P2: 24 hours**
  - **P3: 7 days**

Rationale:
- Pull/poll-first removes the hardest early reliability risks (webhook delivery, idempotency races, callback auth edge cases) while still proving approval-routing value.
- The SLA ladder creates immediate enterprise-operable behavior (escalation expectations + queue hygiene) without requiring full policy complexity on day 1.
- RelayTrace can differentiate fastest on governance-grade supervision contract + auditability, not on broad workflow feature parity.

## 30-day execution plan

### Week 1 (Foundation + contract freeze)
- Freeze v0 `DecisionRequest` / `DecisionState` schema and poll API contract.
- Implement Postgres-backed request lifecycle (`new -> pending -> approved/rejected/escalated/expired`).
- Add strict priority classification (P1/P2/P3) with server-calculated due-at based on locked SLA defaults.
- Ship minimal audit ledger entries for every state transition.

### Week 2 (Supervisor workflow + SLA engine)
- Build operator queue view sorted by urgency: priority, time-to-breach, age.
- Implement escalation scheduler for SLA breach transitions and assignment routing.
- Add clarification loop primitives (`needs_info`, `question`, `response`) in the same request thread.
- Enforce idempotent poll read semantics for workers.

### Week 3 (Agent integration + hardening)
- Deliver reference worker client (Python) using pull/poll-first decision retrieval.
- Add retry-safe polling guidance (backoff + jitter + max staleness budget).
- Implement auth baseline (service tokens, scoped permissions for poll/read/write).
- Add metrics + traces: queue depth, SLA-at-risk counts, decision latency percentiles.

### Week 4 (Pilot + proof)
- Run one constrained pilot flow (security triage or regulated exception adjudication).
- Capture outcomes: SLA adherence, escalation correctness, clarification turnaround, operator load.
- Produce go/no-go memo for next phase (push callback beta, policy DSL, broader domain rollout).

## Exit criteria for day 30
- End-to-end pull/poll-first approval loop working in production-like environment.
- P1/P2/P3 SLA timers and escalations functioning with audit evidence.
- At least one real workflow completed with measurable latency + reliability metrics.
- Clear decision on phase-2 scope with documented risks.

## Next deliverables
1) Source-verified matrix with explicit citations + confidence tags (High/Med/Low)
2) Top-3 wedge options + recommended entry wedge
3) 60–90 day MVP definition
4) Risk register and de-risk plan

## Notes
- This file is intentionally token-light and serves as a durable checkpoint.
- This draft is now updated with a locked execution recommendation and 30-day plan.
- Source of truth for product intent: `docs/APPROVAL_CONTROL_PLANE_SPEC_SEED.md`.
