from __future__ import annotations

from typing import Any, Dict

from adn_v3 import ADNv3
from adn_v3.contracts import v3_types
from adn_v3.contracts.v3_reason_codes import ReasonCode


def test_v3_types_contains_bad_number_good_float_path_is_false():
    # This targets the likely last uncovered line: the "return False" in float branch.
    assert v3_types._contains_bad_number(1.234) is False


def test_v3_parse_events_accepts_metadata_none_and_still_not_error():
    v3 = ADNv3()

    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "meta-none",
        "events": [
            {"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": None},
        ],
    }

    resp = v3.evaluate(req)

    # Valid request should not error
    assert resp["decision"] in {"ALLOW", "WARN", "BLOCK"}
    assert resp["meta"]["fail_closed"] is True


def test_v3_parse_events_json_dumps_failure_fails_closed():
    v3 = ADNv3()

    # sets are not JSON serializable -> json.dumps(...) raises -> fail-closed invalid request
    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "json-fail",
        "events": [
            {"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": {"bad": {1, 2, 3}}},
        ],
    }

    resp = v3.evaluate(req)

    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_request_parsing_generic_exception_path_fails_closed():
    # Force the `except Exception:` branch in ADNv3.evaluate contract parsing
    import adn_v3.core as core

    original = core.ADNv3Request

    class BoomRequest:
        @classmethod
        def from_dict(cls, d: Dict[str, Any]) -> Any:
            raise RuntimeError("boom")

    core.ADNv3Request = BoomRequest  # type: ignore[assignment]
    try:
        v3 = ADNv3()
        resp = v3.evaluate({"contract_version": 3, "component": "adn", "request_id": "x", "events": []})
        assert resp["decision"] == "ERROR"
        assert resp["meta"]["fail_closed"] is True
        assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]
    finally:
        core.ADNv3Request = original  # restore
