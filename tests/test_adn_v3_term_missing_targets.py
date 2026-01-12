from __future__ import annotations

from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode
from adn_v3.contracts.v3_types import ADNv3Request


def test_v3_types_events_list_element_must_be_dict():
    # Targets v3_types.py missing line 57
    bad = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "bad-event-element",
        "events": ["not-a-dict"],
    }

    try:
        ADNv3Request.from_dict(bad)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == ReasonCode.ADN_ERROR_INVALID_REQUEST.value


def test_v3_core_parse_events_metadata_none_path_is_covered():
    # Targets core.py missing line 153 (metadata is None -> {})
    v3 = ADNv3()
    resp = v3.evaluate(
        {
            "contract_version": 3,
            "component": "adn",
            "request_id": "meta-none-branch",
            "events": [
                {"event_type": "PING", "severity": 0.1, "source": "dqsn", "metadata": None},
            ],
        }
    )
    assert resp["decision"] in {"ALLOW", "WARN", "BLOCK"}


def test_v3_core_parse_events_json_dumps_exception_path_is_covered():
    # Targets core.py missing line 171 (json.dumps failure -> invalid request)
    v3 = ADNv3()
    resp = v3.evaluate(
        {
            "contract_version": 3,
            "component": "adn",
            "request_id": "json-dumps-exc-branch",
            "events": [
                {
                    "event_type": "PING",
                    "severity": 0.1,
                    "source": "dqsn",
                    "metadata": {"bad": {1, 2, 3}},  # set is not JSON serializable
                },
            ],
        }
    )
    assert resp["decision"] == "ERROR"
    assert ReasonCode.ADN_ERROR_INVALID_REQUEST.value in resp["reason_codes"]


def test_v3_core_config_fingerprint_exception_fallback_is_covered():
    # Targets core.py missing line 223 (vars(cfg) raises -> {"_": "unavailable"})
    v3 = ADNv3()

    class BadCfg:
        __slots__ = ()

    fp = v3._config_fingerprint(BadCfg())  # type: ignore[arg-type]
    assert fp == {"_": "unavailable"}
