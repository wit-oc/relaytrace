# Transport Spike: Kafka-lite vs NATS JetStream (RelayTrace MVP)

## Scope
Choose the first durable transport for RelayTrace handoff/decision events.

Evaluated options:
- **Kafka-lite**: Redpanda / single-binary Kafka-compatible broker
- **NATS JetStream**: NATS with built-in stream persistence + consumers

## Decision
**Choose NATS JetStream for MVP implementation.**

Kafka-compatible transport remains a vNext option if throughput, partition-sharding, or Kafka ecosystem integration becomes dominant.

## Why JetStream now
1. **Operational simplicity**
   - One lightweight broker process in dev/small-prod.
   - Simple stream/consumer setup for queue-like flows.
2. **Natural fit for request/decision inbox-outbox pattern**
   - Pull consumers map cleanly to supervisor polling and agent poll APIs.
   - Ack/Nak + redelivery semantics are straightforward for at-least-once delivery.
3. **Lower MVP cognitive load**
   - Smaller configuration surface than Kafka (brokers, partitions, retention tuning).
4. **Resource profile**
   - Good footprint for early deployment targets.

## Tradeoff summary
| Criterion | Kafka-lite | JetStream |
|---|---|---|
| Ecosystem maturity | Excellent | Strong but smaller ecosystem |
| Setup complexity | Medium | Low |
| Ordering semantics | Partition-ordered | Subject/stream + consumer ordering |
| Replay tooling | Strong | Good |
| MVP time-to-first-event | Medium | Fast |
| Fit for outbox pull/poll | Good | Excellent |

## Risks & mitigations
- **Risk:** Team familiarity may be higher with Kafka.
  - **Mitigation:** keep event contract transport-agnostic and isolate broker client in adapter layer.
- **Risk:** Future high-throughput fanout constraints.
  - **Mitigation:** define `EventBus` interface now; support Kafka implementation later without API contract break.

## Implementation notes
- Canonical streams (MVP):
  - `relaytrace.handoff.requested`
  - `relaytrace.handoff.decided`
  - `relaytrace.audit.receipt`
- Consumer groups:
  - `relaytrace-supervisor-poller`
  - `relaytrace-agent-decision-poller`
- Delivery semantics: at-least-once, idempotency key = `request_id` (+ decision revision where needed).

## Exit criteria for revisiting decision
Re-open transport decision if one or more occur:
- sustained throughput target exceeds MVP assumptions
- strict Kafka-native enterprise integration becomes mandatory
- JetStream operational behavior fails reliability SLO under load tests

## Status
- Spike status: complete
- Decision type: MVP default transport
- Date: 2026-02-13
