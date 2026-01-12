from __future__ import annotations

from typing import Any, Dict

from .models import TelemetryPacket


"""
Telemetry Adapter – Raw → Structured TelemetryPacket

Different execution environments (full nodes, lightweight nodes,
Sentinel AI, DQSN gateways, test harnesses) expose different raw
telemetry formats.

TelemetryAdapter standardises them into a single TelemetryPacket.

Security/Determinism note:
- We must NOT default missing timestamps to the current system time,
  because that makes identical inputs produce different outputs.
- If timestamp is missing or invalid, we default deterministically to 0.0.
"""


class TelemetryAdapter:
    def parse(self, raw: Dict[str, Any], node_id: str = "unknown") -> TelemetryPacket:
        """
        Convert a raw telemetry dict into a TelemetryPacket.

        Any missing/invalid numeric fields are coerced to safe defaults
        deterministically (0 / 0.0). This keeps the adapter robust and
        prevents non-deterministic behavior.
        """
        if not isinstance(raw, dict):
            raw = {}

        def _to_int(x: Any, default: int = 0) -> int:
            try:
                return int(x)
            except Exception:
                return default

        def _to_float(x: Any, default: float = 0.0) -> float:
            try:
                return float(x)
            except Exception:
                return default

        ts_raw = raw.get("timestamp", 0.0)
        ts = _to_float(ts_raw, 0.0)

        return TelemetryPacket(
            node_id=str(node_id),
            height=_to_int(raw.get("height", 0)),
            mempool_size=_to_int(raw.get("mempool_size", 0)),
            peer_count=_to_int(raw.get("peer_count", 0)),
            timestamp=ts,
            extra={
                k: v
                for k, v in raw.items()
                if k not in {"height", "mempool_size", "peer_count", "timestamp"}
            },
        )
