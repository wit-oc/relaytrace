# RelayTrace MVP Decision Gates

## Purpose
Prevent scope drift and avoid engineering into corners while moving quickly.

This defines explicit **Go / No-Go** checkpoints across phases for the AWS AgentCore + Strands-first MVP.

---

## Phase 0 — Foundation Contract Gate (before deeper build)

### Required outcomes
1. **Event schema v0 locked**
   - `handoff.requested`
   - `handoff.decided`
   - `audit.receipt`
   - versioned envelope fields + compatibility policy

2. **Reliability semantics locked**
   - at-least-once delivery
   - idempotency key strategy (`request_id + version`)
   - retry + DLQ behavior

3. **Lane model locked**
   - `lane_id` required for non-blocking execution
   - per-lane checkpoint contract
   - pause/resume semantics by lane

4. **Authz baseline locked**
   - operator role/scope model
   - reroute authorization constraints
   - immutable audit identity fields

### Go criteria
- All above captured in specs and reviewed once.
- One synthetic request/decision payload pair passes schema validation.

### No-Go signals
- Multiple competing schema drafts still active.
- No clear idempotency strategy.
- Global-pause behavior still implicit.

---

## Phase 1 — Thin Vertical Slice Gate (MVP core)

### Required outcomes
1. **Strands adapter skeleton runs end-to-end**
   - wrapper emits `handoff.requested`
   - RelayTrace receives + routes
   - operator action emits `handoff.decided`
   - agent resumes from checkpoint

2. **Operator queue UX minimal but functional**
   - list queue
   - open item
   - approve/reject/reroute/add-context

3. **Telemetry v1 emitted**
   - HITL invocation rate
   - decision distribution
   - first-response and final-decision latency

4. **Engineering view (minimum)**
   - aggregate ratios + latency table by trigger class

### Go criteria
- 100 synthetic events run, with ~1–5% HITL, and non-blocked lanes keep processing.
- No data loss in request/decision flow under retry scenarios.

### No-Go signals
- HITL for one item halts unrelated work.
- Decision callback correlation failures.
- No trustworthy telemetry for decision outcomes.

---

## Phase 2 — Reliability and Ops Hardening Gate

### Required outcomes
1. Backpressure behavior validated
   - queue depth alarms
   - lane-level timeout policies
   - escalation on missed response SLA

2. Failure-mode coverage
   - duplicate events
   - delayed decisions
   - missing checkpoint refs
   - dead-letter processing path

3. Observability baseline
   - trace IDs across adapter/control plane
   - per-stage latency metrics
   - operator action audit completeness

### Go criteria
- Soak test passes with sustained throughput and no global stalls.
- Escalation and timeout paths are deterministic and observable.

### No-Go signals
- Unbounded queue growth without graceful degradation.
- Incomplete audit records for any decision path.

---

## Phase 3 — Pilot Readiness Gate

### Required outcomes
1. Security baseline complete
   - signed payloads or mTLS
   - scoped credentials
   - sensitive payload redaction in operator surfaces

2. Multi-team readiness
   - role-based queue isolation
   - operator-vs-engineering dashboard separation
   - tenant/workspace boundary checks

3. Pilot playbook
   - incident response path
   - rollback plan
   - success/failure KPIs with target ranges

### Go criteria
- Pilot checklist complete and reviewed.
- One controlled pilot domain selected (infra-oriented).

### No-Go signals
- Undefined ownership for escalations/incidents.
- Dashboard data model not trusted by operators or engineers.

---

## Corner-avoidance decisions (must stay fixed unless major version)
1. Event versioning + backward compatibility policy
2. Lane-scoped non-blocking contract
3. Immutable minimum audit envelope
4. Request/decision correlation + idempotency semantics
5. Persona-separated operator/engineering data model

---

## Suggested KPI starter thresholds (tune later)
- Decision callback success: >99.5%
- Lost/unmatched decision events: <0.1%
- P95 time-to-first-human-action: by priority class
- Queue stale rate: <2% over policy threshold window
- HITL invocation rate trend: stable or improving by trigger class

---

## Current recommendation
Proceed with a narrow MVP:
- AWS AgentCore + Strands adapter only
- One primary stream transport mode
- One operator queue workflow
- One engineering metrics panel focused on HITL quality and latency

Defer broad policy DSL, multi-cloud, and advanced mission-control visual complexity until post-MVP proof.
