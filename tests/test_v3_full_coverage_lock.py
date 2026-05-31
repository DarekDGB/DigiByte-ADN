from __future__ import annotations

from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode
from adn_v3.contracts.v3_types import ADNv3Request


def test_v3_request_rejects_non_integer_contract_version() -> None:
    try:
        ADNv3Request.from_dict(
            {
                "contract_version": "3",
                "component": "adn",
                "request_id": "bad-version-type",
                "events": [],
            }
        )
        assert False, "Expected ValueError for non-integer contract_version"
    except ValueError as exc:
        assert str(exc) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_parse_events_rejects_non_dict_event_defensively() -> None:
    v3 = ADNv3()

    try:
        v3._parse_events(["not-an-event-dict"])  # type: ignore[list-item]
        assert False, "Expected ValueError for non-dict event"
    except ValueError as exc:
        assert str(exc) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_parse_events_rejects_blank_source_defensively() -> None:
    v3 = ADNv3()

    try:
        v3._parse_events(
            [
                {
                    "event_type": "PING",
                    "severity": 0.1,
                    "source": "   ",
                    "metadata": {},
                }
            ]
        )
        assert False, "Expected ValueError for blank source"
    except ValueError as exc:
        assert str(exc) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_decision_unknown_state_falls_back_to_block() -> None:
    v3 = ADNv3()

    class UnknownState:
        risk_level = object()
        lockdown_state = object()

    assert v3._decision_from_state(UnknownState()) == "BLOCK"  # type: ignore[arg-type]
