from adn_v2.engine import evaluate_defense
from adn_v2.models import DefenseEvent, NodeDefenseConfig, NodeDefenseState
from adn_v3 import ADNv3


def test_v2_v3_no_behavior_drift_minimal_events():
    cfg = NodeDefenseConfig()

    events = [
        DefenseEvent(event_type="REORG_WARNING", severity=0.60, source="dqsn", metadata={"depth": 2}),
        DefenseEvent(event_type="PROPAGATION_ANOMALY", severity=0.55, source="sentinel", metadata={"lat_ms": 900}),
    ]

    # v2 direct
    v2_state = evaluate_defense(events=events, config=cfg, state=NodeDefenseState())

    # v3 wrapper
    v3 = ADNv3(config=cfg)
    req = {
        "contract_version": 3,
        "component": "adn",
        "request_id": "no-drift",
        "events": [
            {"event_type": "REORG_WARNING", "severity": 0.60, "source": "dqsn", "metadata": {"depth": 2}},
            {"event_type": "PROPAGATION_ANOMALY", "severity": 0.55, "source": "sentinel", "metadata": {"lat_ms": 900}},
        ],
    }
    resp = v3.evaluate(req)

    assert resp["decision"] in {"ALLOW", "WARN", "BLOCK"}  # must not error for valid input
    assert resp["risk"]["level"] == v2_state.risk_level.value
    assert resp["risk"]["lockdown_state"] == v2_state.lockdown_state.value
