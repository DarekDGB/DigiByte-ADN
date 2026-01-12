from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Optional


ADN_LAYER_NAME = "ADN_v2"


def _decision_to_str(decision: Any) -> str:
    """
    Convert a decision-like value to a string safely.

    We intentionally do NOT import a missing `Decision` enum/module.
    Supported inputs:
    - Enum-like: has `.value`
    - string
    - anything else: str(x)
    """
    if hasattr(decision, "value"):
        try:
            return str(getattr(decision, "value"))
        except Exception:
            return str(decision)
    return str(decision)


@dataclass
class AdaptiveEvent:
    """
    Generic adaptive event emitted by ADN v2.

    This structure is designed to be compatible with the
    DigiByte-Quantum-Adaptive-Core RiskEvent model.

    Determinism note:
    - `created_at` is wall-clock time (UTC). It is for observability/audit trails
      and MUST NOT be used inside any deterministic contract hashing.
    """

    event_id: str
    layer: str
    decision: str
    fingerprint: str
    severity: float
    created_at: datetime
    feedback: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # datetime → ISO string for JSON / logging
        d["created_at"] = self.created_at.isoformat()
        return d


def build_adaptive_event_from_adn(
    *,
    event_id: str,
    decision: Any,
    severity: float,
    fingerprint: str,
    node_id: Optional[str] = None,
    reason: Optional[str] = None,
    extra_meta: Optional[Dict[str, Any]] = None,
    created_at: Optional[datetime] = None,
) -> AdaptiveEvent:
    """
    Create an AdaptiveEvent instance from an ADN decision.

    - event_id    – unique id in your system (tx id, internal uuid, etc.)
    - decision    – enum-like or string (converted to str safely)
    - severity    – numeric signal 0.0–1.0 (clamped)
    - fingerprint – hash / identifier of the underlying situation
    - node_id     – optional identifier of this ADN node
    - reason      – optional human-readable reason from ADN engine
    - extra_meta  – any additional fields you want to send
    - created_at  – optional override (useful for deterministic tests)
    """
    meta: Dict[str, Any] = {}
    if node_id is not None:
        meta["node_id"] = node_id
    if reason is not None:
        meta["reason"] = reason
    if extra_meta:
        meta.update(extra_meta)

    # Wall-clock timestamp for audit/trace only (not contract hashing)
    ts = created_at or datetime.utcnow()

    return AdaptiveEvent(
        event_id=str(event_id),
        layer=ADN_LAYER_NAME,
        decision=_decision_to_str(decision),
        fingerprint=str(fingerprint),
        severity=max(0.0, min(1.0, float(severity))),
        created_at=ts,
        metadata=meta,
    )


# --------------------------------------------------------------------------- #
# Optional: simple helper to send events into Adaptive Core
# --------------------------------------------------------------------------- #

AdaptiveSink = Callable[[AdaptiveEvent], None]


def emit_adaptive_event(
    sink: Optional[AdaptiveSink],
    *,
    event_id: str,
    decision: Any,
    severity: float,
    fingerprint: str,
    node_id: Optional[str] = None,
    reason: Optional[str] = None,
    extra_meta: Optional[Dict[str, Any]] = None,
    created_at: Optional[datetime] = None,
) -> Optional[AdaptiveEvent]:
    """
    Convenience helper for ADN:

    If `sink` is provided, build an AdaptiveEvent and send it there.
    If `sink` is None → do nothing and return None.

    Example usage from ADN engine / policies:

        emit_adaptive_event(
            adaptive_sink,
            event_id=request_id,
            decision=decision,
            severity=risk_score,
            fingerprint=primary_fingerprint,
            node_id=node_id,
            reason=reason,
        )
    """
    if sink is None:
        return None

    event = build_adaptive_event_from_adn(
        event_id=event_id,
        decision=decision,
        severity=severity,
        fingerprint=fingerprint,
        node_id=node_id,
        reason=reason,
        extra_meta=extra_meta,
        created_at=created_at,
    )
    sink(event)
    return event
