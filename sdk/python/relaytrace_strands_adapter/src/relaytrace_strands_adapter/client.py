from dataclasses import asdict
from typing import Optional

from .types import HandoffDecision, HandoffRequest


class RelayTraceDecisionClient:
    """Stub client for RelayTrace outbox pull/poll operations."""

    def __init__(self, base_url: str, token: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def emit_handoff_request(self, request: HandoffRequest) -> dict:
        """Placeholder emitter; wire to /v1/hitl/requests in implementation phase."""
        return {"status": "stub", "request": asdict(request)}

    def poll_decision(self, consumer_id: str, max_items: int = 1) -> dict:
        """Placeholder long-poll; wire to /v1/outbox/{outbox}/pull."""
        return {
            "status": "stub",
            "consumer_id": consumer_id,
            "max_items": max_items,
            "items": [],
        }

    def ack_decision(self, message_id: str, consumer_id: str) -> dict:
        """Placeholder ack; wire to /v1/outbox/{outbox}/ack."""
        return {
            "status": "stub",
            "message_id": message_id,
            "consumer_id": consumer_id,
        }

    def apply_decision(self, decision: HandoffDecision) -> dict:
        """Placeholder continuation mapping entrypoint."""
        return {"status": "stub", "decision": asdict(decision)}
