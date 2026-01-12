from __future__ import annotations

import types

from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode
from adn_v3.contracts.v3_types import ADNv3Request


def test_v3_types_rejects_non_dict_request():
    try:
        ADNv3Request.from_dict("not-a-dict")  # type: ignore[arg-type]
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_types_rejects_unknown_top_level_keys():
    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "x",
        "events": [],
        "unknown": "nope",
    }
    try:
        ADNv3Request.from_dict(req)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_UNKNOWN_KEY.value


def test_v3_types_rejects_blank_component_and_request_id_and_bad_events_type():
    # blank component
    try:
        ADNv3Request.from_dict({"contract_version": 3, "component": "   ", "request_id": "x", "events": []})
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value

    # blank request_id
    try:
        ADNv3Request.from_dict({"contract_version": 3, "component": "adn", "request_id": "   ", "events": []})
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value

    # events not a list
    try:
        ADNv3Request.from_dict({"contract_version": 3, "component": "adn", "request_id": "x", "events": "nope"})
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_types_rejects_event_not_dict_and_nested_infinity():
    # event element not dict
    try:
        ADNv3Request.from_dict({"contract_version": 3, "component": "adn", "request_id": "x", "events": ["bad"]})
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value

    # nested infinity (covers float("inf") branch)
    try:
        ADNv3Request.from_dict(
            {
                "contract_version": 3,
                "component": "adn",
                "request_id": "x",
                "events": [{"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": {"x": [float("inf")]}}],
            }
        )
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_BAD_NUMBER.value


def test_v3_core_helper_branches_decision_action_config_fingerprint():
    v3 = ADNv3()

    # Cover _action_to_dict with missing attributes
    dummy_action = types.SimpleNamespace()
    d = v3._action_to_dict(dummy_action)
    assert d["action_type"] == ""
    assert d["reason"] == ""
    assert d["metadata"] is None

    # Cover _config_fingerprint exception branch by passing object that breaks vars()
    class BadCfg:
        __slots__ = ()  # vars() will raise TypeError

    fp = v3._config_fingerprint(BadCfg())  # type: ignore[arg-type]
    assert fp == {"_": "unavailable"}

    # Cover _decision_from_state branches using a minimal fake state
    class FakeState:
        def __init__(self, risk_level, lockdown_state):
            self.risk_level = risk_level
            self.lockdown_state = lockdown_state

    # Import enums from v2 models (they are the ones core uses)
    from adn_v2.models import RiskLevel, LockdownState

    assert v3._decision_from_state(FakeState(RiskLevel.NORMAL, LockdownState.NONE)) in {"ALLOW", "WARN", "BLOCK"}
    assert v3._decision_from_state(FakeState(RiskLevel.ELEVATED, LockdownState.NONE)) == "WARN"
    assert v3._decision_from_state(FakeState(RiskLevel.CRITICAL, LockdownState.NONE)) == "BLOCK"
    assert v3._decision_from_state(FakeState(RiskLevel.NORMAL, LockdownState.PARTIAL)) == "WARN"
    assert v3._decision_from_state(FakeState(RiskLevel.NORMAL, LockdownState.FULL)) == "BLOCK"
