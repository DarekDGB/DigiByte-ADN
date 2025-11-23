from __future__ import annotations

import json
from typing import Any, Dict

from .engine import ADNEngine


class ADNServer:
    """
    Minimal, framework-agnostic server wrapper.

    Real integrations can plug this into FastAPI, Flask, or a raw HTTP server.
    Here we only define pure-Python handlers that accept dicts and return dicts.
    """

    def __init__(self, engine: ADNEngine) -> None:
        self.engine = engine

    def handle_telemetry(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        decision = self.engine.process_raw_telemetry(payload)
        return {
            "node_id": self.engine.state.node_id,
            "level": decision.level.value,
            "score": decision.score,
            "reason": decision.reason,
            "actions": decision.actions,
        }

    def handle_health(self) -> Dict[str, Any]:
        state = self.engine.state
        return {
            "node_id": state.node_id,
            "hardened_mode": state.hardened_mode,
            "last_decision": {
                "level": state.last_decision.level.value,
                "score": state.last_decision.score,
            }
            if state.last_decision
            else None,
        }

    def handle_raw_request(self, body: str) -> str:
        payload = json.loads(body)
        if payload.get("type") == "telemetry":
            response = self.handle_telemetry(payload["data"])
        else:
            response = self.handle_health()
        return json.dumps(response)
