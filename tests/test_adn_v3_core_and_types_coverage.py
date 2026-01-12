from __future__ import annotations

from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode
from adn_v3.contracts.v3_types import ADNv3Request


def test_v3_valid_request_happy_path_not_error():
    v3 = ADNv3()

    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "happy",
        "events": [
            {"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": {"a": 1}},
        ],
    }

    resp = v3.evaluate(req)

    # Must be a non-error decision for valid inputs
    assert resp["decision"] in {"ALLOW", "WARN", "BLOCK"}
    assert resp["contract_version"] == 3
    assert resp["component"] == "adn"
    assert resp["request_id"] == "happy"
    assert resp["meta"]["fail_closed"] is True
    assert isinstance(resp["context_hash"], str)
    assert len(resp["context_hash"]) == 64  # sha256 hex


def test_v3_component_mismatch_fails_closed():
    v3 = ADNv3()

    req = {
        "contract_version": 3,
        "component": "not-adn",
        "request_id": "cmp",
        "events": [],
    }

    resp = v3.evaluate(req)

    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_event_missing_required_fields_fails_closed():
    v3 = ADNv3()

    # Missing event_type/source, invalid schema
    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "bad-event",
        "events": [{"severity": 0.5, "metadata": {}}],
    }

    resp = v3.evaluate(req)

    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_event_bad_severity_range_fails_closed():
    v3 = ADNv3()

    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "bad-sev",
        "events": [{"event_type": "PING", "severity": 2.0, "source": "dqsn", "metadata": {}}],
    }

    resp = v3.evaluate(req)

    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_event_metadata_not_dict_fails_closed():
    v3 = ADNv3()

    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "bad-meta",
        "events": [{"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": "nope"}],
    }

    resp = v3.evaluate(req)

    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_types_rejects_bad_numbers_nested_structures():
    # Covers v3_types recursion branches (dict + list)
    bad = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "bn",
        "events": [{"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": {"x": [1, float("nan")]}}],
    }

    try:
        ADNv3Request.from_dict(bad)
        assert False, "Expected ValueError for bad numbers"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_BAD_NUMBER.value
