"""
Basic tests for the ADN v2 policy engine.

Covers:
- Loading default policies
- Applying a synthetic risk packet
- Ensuring policy decisions return expected fields
"""

import sys
from pathlib import Path

# Ensure src/ is on path
def _ensure_src():
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))

_ensure_src()

from adn_v2.policy import PolicyEngine
from adn_v2.models import RiskPacket


def test_policy_engine_loads():
    """Policy engine should initialize with default rules."""
    engine = PolicyEngine()
    assert engine is not None
    assert isinstance(engine.rules, dict)
    assert len(engine.rules) > 0


def test_policy_simple_risk_eval():
    """Policy engine should return a valid decision object."""
    engine = PolicyEngine()

    packet = RiskPacket(
        entropy_score=0.42,
        reorg_depth=0,
        mempool_bloat=0.1,
        timestamp=1234567890,
        source="test"
    )

    decision = engine.evaluate(packet)

    assert decision is not None
    assert hasattr(decision, "level")
    assert hasattr(decision, "actions")
    assert decision.level in ["NORMAL", "ELEVATED", "HIGH", "CRITICAL"]
    assert isinstance(decision.actions, list)
