import pytest
from adn_v2.models import DefenseEvent, NodeDefenseConfig
from adn_v2.engine import evaluate_defense
from adn_v2.actions import build_rpc_policy_from_state
from adn_v2.models import LockdownState, RiskLevel


def test_defense_flow_partial_lockdown():
    events = [
        DefenseEvent(event_type="rpc_abuse", severity=0.6, source="local"),
        DefenseEvent(event_type="sentinel_alert", severity=0.5, source="sentinel"),
    ]

    state = evaluate_defense(events, NodeDefenseConfig())
    policy = build_rpc_policy_from_state(state)

    assert state.risk_level == RiskLevel.ELEVATED
    assert state.lockdown_state == LockdownState.PARTIAL
    assert policy["rpc_rate_limit"] == 100
    assert "PARTIAL_LOCKDOWN" in policy["notes"][0]


def test_defense_flow_full_lockdown():
    events = [
        DefenseEvent(event_type="dqsn_critical", severity=0.9, source="dqsn"),
        DefenseEvent(event_type="rpc_abuse", severity=0.85, source="local"),
    ]

    state = evaluate_defense(events, NodeDefenseConfig())
    policy = build_rpc_policy_from_state(state)

    assert state.risk_level == RiskLevel.CRITICAL
    assert state.lockdown_state == LockdownState.FULL
    assert policy["rpc_enabled"] is False
