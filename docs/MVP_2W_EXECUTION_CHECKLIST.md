# RelayTrace MVP — 2-Week Execution Checklist

Aligned to: `docs/MVP_DECISION_GATES.md`

## 14-Day Plan (single stream, AgentCore + Strands-first)

| Day(s) | Gate | Task | Owner Role | Exit Criteria |
|---|---|---|---|---|
| 1 | Phase 0 — Foundation Contract | Lock event envelope v0 for `handoff.requested`, `handoff.decided`, `audit.receipt` (+ version/compatibility rules). | Staff Backend Engineer | Schema docs committed; example payloads validate; one review sign-off recorded. |
| 1-2 | Phase 0 — Foundation Contract | Lock reliability semantics: at-least-once delivery, idempotency key (`request_id+version`), retry/DLQ contract. | Platform Engineer | Reliability section merged; duplicate replay test spec written; DLQ routing defined. |
| 2 | Phase 0 — Foundation Contract | Lock lane model: required `lane_id`, per-lane checkpoints, pause/resume semantics. | Workflow Architect | Lane contract added to spec; non-blocking lane behavior explicitly documented. |
| 2 | Phase 0 — Foundation Contract | Lock authz baseline: operator scopes, reroute constraints, immutable audit identity fields. | Security Engineer | Authz matrix approved; immutable audit identity fields listed and frozen. |
| 3 | Phase 0 — Foundation Contract (Go check) | Run schema validation on synthetic request/decision pair and publish gate decision note. | Tech Lead | Validation passes end-to-end; Phase 0 Go logged with links. |
| 3-4 | Phase 1 — Thin Vertical Slice | Implement Strands adapter skeleton to emit `handoff.requested` + correlation metadata. | Adapter Engineer | Adapter emits valid events in dev; correlation IDs present in logs. |
| 4-5 | Phase 1 — Thin Vertical Slice | Implement RelayTrace intake/routing + decision callback (`handoff.decided`) to checkpoint resume path. | Control Plane Engineer | One synthetic handoff round trip resumes agent lane successfully. |
| 5-6 | Phase 1 — Thin Vertical Slice | Build minimal operator queue UX: list queue, open item, approve/reject/reroute/add-context. | Full-Stack Engineer | Operator can complete all four decision actions from UI/API path. |
| 6-7 | Phase 1 — Thin Vertical Slice | Emit telemetry v1: HITL invocation rate, decision distribution, first-response/final-decision latency. | Observability Engineer | Metrics emitted to dashboard backend with stable labels. |
| 7 | Phase 1 — Thin Vertical Slice | Add engineering view (aggregate ratios + latency by trigger class). | Analytics Engineer | Dashboard panel available and query-backed; trigger-class breakdown visible. |
| 8 | Phase 1 — Thin Vertical Slice (Go check) | Execute 100 synthetic events (~1–5% HITL), verify non-blocking lanes and no data loss under retries. | QA/Perf Engineer | Test report shows pass on event count, correlation, and non-blocking criteria. |
| 9-10 | Phase 2 — Reliability/Ops Hardening | Validate backpressure controls: queue depth alarms, lane timeout policies, escalation on missed SLA. | SRE | Alarm + escalation runbook tested; timeout policy enforced in staging. |
| 10-11 | Phase 2 — Reliability/Ops Hardening | Cover failure modes: duplicate events, delayed decisions, missing checkpoint refs, DLQ processing. | Reliability Engineer | Automated tests pass for all four failure modes; DLQ replay path documented. |
| 11-12 | Phase 2 — Reliability/Ops Hardening | Establish observability baseline: trace IDs across adapter/control plane, per-stage latency, audit completeness. | Observability Engineer | End-to-end traces queryable; audit completeness checks green. |
| 13 | Phase 2 — Reliability/Ops Hardening (Go check) | Soak test sustained throughput; verify deterministic escalation/timeout paths and no global stalls. | QA/Perf Engineer + SRE | Soak report passes throughput/stability thresholds; Phase 2 Go logged. |
| 14 | Phase 3 — Pilot Readiness (prep checkpoint) | Draft pilot readiness packet: security baseline checklist, ownership/escalation map, pilot KPI targets, rollback path. | Product + Tech Lead + Security | Pilot packet complete and reviewed; No-Go risks explicitly tracked for next phase. |

## Daily Operating Cadence (2 weeks)

- **Daily 15 min standup:** blocker scan for schema/reliability/lane/authz invariants.
- **Daily 10 min metrics review:** HITL volume, stale queue, callback mismatch rate.
- **Twice-weekly risk review:** unresolved No-Go signals from decision gates.

## Fixed Corner-Avoidance Checks (must not drift)

Validate these in code review templates and gate reviews:

1. Event versioning + backward compatibility policy remains explicit.
2. Lane-scoped non-blocking contract is preserved.
3. Minimum immutable audit envelope remains intact.
4. Request/decision correlation + idempotency semantics remain deterministic.
5. Operator vs engineering persona-separated data model stays enforced.
