from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskSignal:
    source: str
    level: RiskLevel
    score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryPacket:
    node_id: str
    height: int
    mempool_size: int
    peer_count: int
    timestamp: float
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    level: RiskLevel
    score: float
    reason: str
    actions: List[str] = field(default_factory=list)


@dataclass
class NodeState:
    node_id: str
    hardened_mode: bool = False
    last_decision: Optional[PolicyDecision] = None


@dataclass
class ActionResult:
    name: str
    success: bool
    detail: str = ""
