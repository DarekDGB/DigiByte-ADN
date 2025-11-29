from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    """
    High-level risk classification used by ADN v2.

    The engine and policy helpers use this to describe how serious the
    current situation is for a node:
    - NORMAL   – routine operation
    - ELEVATED – something looks off, apply extra caution
    - HIGH     – strong indication of abuse or attack
    - CRITICAL – emergency state, strongest defenses should engage
    """

    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"


# Backwards-compatible alias for older modules.
# Anywhere that imported `RiskState` will now get the same Enum.
RiskState = RiskLevel


@dataclass
class RiskSignal:
    """
    Normalised risk signal derived from raw telemetry.

    Examples:
    - source="telemetry", level=RiskLevel.ELEVATED
    - source="sentinel",  level=RiskLevel.HIGH
    """

    source: str
    level: RiskLevel
    score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryPacket:
    """
    Minimal snapshot of node health used by ADN v2.

    This is what the node feeds into the engine; the validator then turns
    it into one or more RiskSignal entries.
    """

    node_id: str
    height: int
    mempool_size: int
    peer_count: int
    timestamp: float
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    """
    Result of the risk-policy step for classic ADN v2.

    It combines:
    - the chosen RiskLevel,
    - a numeric score, and
    - a human-readable reason plus a list of suggested actions.
    """

    level: RiskLevel
    score: float
    reason: str
    actions: List[str] = field(default_factory=list)


@dataclass
class NodeState:
    """
    Lightweight, in-memory state for a defended node.

    The engine updates this after every decision so callers can see the
    last applied PolicyDecision and whether hardened_mode is active.
    """

    node_id: str
    hardened_mode: bool = False
    last_decision: Optional[PolicyDecision] = None


@dataclass
class ActionResult:
    """
    Outcome of executing a concrete defense action.

    This is intentionally simple: callers can record whether an action
    succeeded and include optional extra detail for logging.
    """

    name: str
    success: bool
    detail: str = ""


# --- v2 defense-layer models (lockdown + actions) ---


class LockdownState(str, Enum):
    """
    Lockdown mode for the node.

    NONE    – no additional restrictions
    PARTIAL – throttling / cool-downs, but RPC still available
    FULL    – strongest mode, e.g. RPC disabled or node isolated
    """

    NONE = "NONE"
    PARTIAL = "PARTIAL"
    FULL = "FULL"


@dataclass
class DefenseEvent:
    """
    Single security-related event observed by ADN.

    Typical event_type values:
    - "rpc_abuse"
    - "withdrawal_spike"
    - "sentinel_alert"
    - "dqsn_critical"
    """

    event_type: str
    severity: float  # 0.0 – 1.0
    source: str      # local, sentinel, dqsn, wallet_guard, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NodeDefenseConfig:
    """
    Configuration knobs for the v2 defense engine.

    The thresholds are intentionally simple so node operators and DigiByte
    devs can tune behaviour without touching the core logic.
    """

    lockdown_threshold: float = 0.75
    partial_lock_threshold: float = 0.5
    max_withdrawals_per_min: int = 50
    rpc_rate_limit: int = 1000  # requests per minute


@dataclass
class DefenseAction:
    """
    Action that ADN decides to take in response to events.

    Examples:
    - "ENTER_PARTIAL_LOCKDOWN"
    - "ENTER_FULL_LOCKDOWN"
    - "LIFT_LOCKDOWN"
    - "THROTTLE_RPC"
    """

    action_type: str
    reason: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class NodeDefenseState:
    """
    Current v2 defense view of the node.

    It tracks:
    - the current RiskLevel,
    - which LockdownState is active, and
    - a list of active events and most recent actions.
    """

    risk_level: RiskLevel = RiskLevel.NORMAL
    lockdown_state: LockdownState = LockdownState.NONE
    active_events: List[DefenseEvent] = field(default_factory=list)
    last_actions: List[DefenseAction] = field(default_factory=list)
