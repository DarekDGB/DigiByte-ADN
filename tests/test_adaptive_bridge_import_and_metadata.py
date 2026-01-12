from __future__ import annotations

from datetime import datetime, timezone

from adn_v2.adaptive_bridge import AdaptiveEvent, build_adaptive_event_from_adn


def test_adaptive_bridge_imports_and_builds_event_without_decision_enum():
    # This must work even if there is no `adn_v2.decisions` module.
    fixed_time = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    ev = build_adaptive_event_from_adn(
        event_id="e1",
        decision="ALLOW",
        severity=0.5,
        fingerprint="fp",
        node_id="node-a",
        reason="ok",
        extra_meta={"x": 1},
        created_at=fixed_time,
    )

    assert isinstance(ev, AdaptiveEvent)
    assert ev.event_id == "e1"
    assert ev.decision == "ALLOW"
    assert ev.severity == 0.5
    assert ev.fingerprint == "fp"
    assert ev.metadata["node_id"] == "node-a"
    assert ev.metadata["reason"] == "ok"
    assert ev.metadata["x"] == 1
    assert ev.created_at == fixed_time


def test_adaptive_event_metadata_is_not_shared_between_instances():
    e1 = build_adaptive_event_from_adn(
        event_id="a",
        decision="WARN",
        severity=0.1,
        fingerprint="fp1",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
    )
    e2 = build_adaptive_event_from_adn(
        event_id="b",
        decision="WARN",
        severity=0.2,
        fingerprint="fp2",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
    )

    e1.metadata["mutate"] = True

    assert "mutate" in e1.metadata
    assert "mutate" not in e2.metadata
