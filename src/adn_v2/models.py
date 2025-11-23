from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class RiskLevel(str, Enum):
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SentinelSignal:
    """
    Normalised signal coming from Sentinel AI v2.

    risk_score: 0.0 – 1.0
    level: mapped RiskLevel based on Sentinel's internal logic
    """

    risk_score: float
    level: RiskLevel
    details: Dict[str, float]


@dataclass
class GuardianSignal:
    """
    Aggregated view from Wallet Guardian.

    wallet_id can be a pseudo-ID, not a real address (privacy-friendly).
    """

    wallet_id: str
    level: RiskLevel
    reasons: List[str]


@dataclass
class ChainSnapshot:
    """
    Lightweight view of current chain / node health.

    This replaces a full node object and keeps ADN decoupled.
    """

    best_height: int
    reorg_depth: int
    mempool_size: int
    orphan_rate: float
    peer_count: int


@dataclass
class DefenseDecision:
    """
    The final decision that ADN v2 hands to the node / infra layer.
    """

    final_level: RiskLevel
    combined_risk: float

    # Actions (all optional flags – actual implementation is outside ADN v2)
    activate_hardened_mode: bool = False
    enforce_pqc: bool = False
    tighten_peer_policy: bool = False
    delay_new_txs: bool = False
    broadcast_warning: bool = False

    # For logs / dashboards
    rationale: str = ""
    tags: Optional[List[str]] = None
