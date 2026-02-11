# RelayTrace

**Mission Control for Agent Handoffs, Approvals, and Auditability.**

RelayTrace is an agent-supervision control plane focused on:
- approval routing and escalation,
- human-in-the-loop clarification,
- structured decision callbacks to agents,
- observability and audit trails across agent workflows.

## Current status
Early architecture/spec repository (public build-in-the-open).

## Why this exists
Most workflow products handle generic approvals, but autonomous agent systems need a dedicated supervisory layer with explicit handoff semantics and governance controls.

## Initial focus
- Infrastructure/agentic platform workloads
- AWS AgentCore-aligned integrations first
- Self-hosted-first architecture with durable components

## Repo structure
- `docs/` — vision, architecture, feasibility notes
- `specs/` — event and callback contracts
- `templates/` — wrapper/decorator and approval-card templates
- `sdk/` — reference integration code
- `examples/` — minimal usage examples

## Brand/imagery concept notes
- Baton handoff metaphor (relay race)
- Hybrid circuitry + human silhouette motifs
- Mission-control operations board aesthetic


## New core docs
- `docs/ARCHITECTURE_TWO_LAYER.md` — AgentCore/Strands substrate vs RelayTrace supervisory plane
- `specs/AWS_AGENTCORE_STRANDS_ADAPTER_SPEC.md` — adapter contract and HITL payload flow
