from __future__ import annotations

import ast
from pathlib import Path

from adn_v3 import ADNv3
from adn_v3.contracts.v3_reason_codes import ReasonCode


def test_adn_v3_engine_can_be_constructed() -> None:
    engine = ADNv3()
    assert engine.COMPONENT == "adn"
    assert engine.CONTRACT_VERSION == 3


def test_adn_v3_default_empty_event_state_allows_deterministically() -> None:
    engine = ADNv3()
    response = engine.evaluate(
        {
            "contract_version": 3,
            "component": "adn",
            "request_id": "basic-policy-current-v3",
            "events": [],
        }
    )

    assert response["contract_version"] == 3
    assert response["component"] == "adn"
    assert response["request_id"] == "basic-policy-current-v3"
    assert response["decision"] == "ALLOW"
    assert response["reason_codes"] == [ReasonCode.ADN_OK.value]
    assert response["meta"]["fail_closed"] is True


def test_tests_directory_has_no_uncollected_test_functions() -> None:
    tests_root = Path(__file__).resolve().parent
    offenders: list[str] = []

    for path in sorted(tests_root.rglob("*.py")):
        if path.name == "__init__.py" or path.name.startswith("test_"):
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        has_test_function = any(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
            for node in ast.walk(tree)
        )
        if has_test_function:
            offenders.append(str(path.relative_to(tests_root.parent)))

    assert offenders == []
