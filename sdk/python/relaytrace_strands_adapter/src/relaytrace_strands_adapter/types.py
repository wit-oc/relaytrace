from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class HandoffRequest:
    request_id: str
    trace_id: str
    agent_id: str
    intent_summary: str
    risk_level: str
    confidence: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HandoffDecision:
    request_id: str
    trace_id: str
    status: str  # approved|rejected|rerouted|needs_info
    operator_id: str
    guidance: Optional[str] = None
    constraints: List[str] = field(default_factory=list)
