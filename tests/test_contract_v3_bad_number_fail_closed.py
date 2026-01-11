from adn_v2.config import ADNConfig
from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode


def test_contract_v3_nan_fails_closed():
    v3 = ADNv3(config=ADNConfig())

    request = {
        "contract_version": 3,
        "request_id": "test",
        "component": "adn",
        "events": [{"metric": float("nan")}],  # NaN on purpose
    }

    response = v3.evaluate(request)

    assert response["decision"] == "ERROR"
    assert response["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_BAD_NUMBER.value in response["reason_codes"]


def test_contract_v3_infinity_fails_closed():
    v3 = ADNv3(config=ADNConfig())

    request = {
        "contract_version": 3,
        "request_id": "test",
        "component": "adn",
        "events": [{"metric": float("inf")}],  # Infinity on purpose
    }

    response = v3.evaluate(request)

    assert response["decision"] == "ERROR"
    assert response["meta"]["fail_closed"] is True
    assert ReasonCode.ADN_ERROR_BAD_NUMBER.value in response["reason_codes"]
