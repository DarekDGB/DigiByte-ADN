from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskState(str, Enum):
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SentinelSignal:
    """
    Normalised output from Sentinel AI v2.

    risk_score: 0.0 – 1.0 inclusive
    details: free-form metadata (triggers, metrics, etc.)
    """

    risk_state: RiskState
    risk_score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalletSignal:
    """
    Aggregated input from Wallet Guardian (Layer 4).

    aggregated_state: worst-case state across all participating wallets.
    wallet_ids: list of wallet identifiers contributing to this state.
    """

    aggregated_state: RiskState
    wallet_ids: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChainTelemetry:
    """
    Lightweight snapshot of chain-level metrics used by ADN v2.

    This is intentionally minimal and implementation-agnostic.
    """

    height: int
    difficulty: float
    mempool_size: int
    avg_block_interval_sec: float
    reorg_depth: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    """
    Result of the policy engine before turning into concrete actions.
    """

    effective_state: RiskState
    hardened_mode: bool = False
    pqc_enforced: bool = False
    peer_filtering: bool = False
    fee_multiplier: float = 1.0
    notes: str = ""


@dataclass
class ActionPlan:
    """
    Machine-readable instruction set that node software can consume.

    All actions are expressed as data. ADN v2 does not directly
    modify DigiByte Core – it emits a plan that integrators apply.
    """

    decision: PolicyDecision
    # Example actions – integrators can extend this structure.
    set_min_fee_rate: Optional[float] = None
    enable_pqc: bool = False
    enable_hardened_mode: bool = False
    drop_peers: List[str] = field(default_factory=list)
    prefer_peers: List[str] = field(default_factory=list)
    broadcast_advisory: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
