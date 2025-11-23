from __future__ import annotations

from typing import Dict, List

from .actions import ActionExecutor
from .models import NodeState, PolicyDecision, RiskSignal, TelemetryPacket
from .policy import PolicyEngine
from .telemetry import TelemetryAdapter
from .validator import RiskValidator  # already created earlier


class ADNEngine:
    """
    Core ADN v2 engine.

    Pipeline:
      telemetry -> RiskValidator -> PolicyEngine -> ActionExecutor
    """

    def __init__(
        self,
        node_id: str,
        policy_engine: PolicyEngine | None = None,
        action_executor: ActionExecutor | None = None,
        validator: RiskValidator | None = None,
        telemetry_adapter: TelemetryAdapter | None = None,
    ) -> None:
        self.state = NodeState(node_id=node_id)
        self.policy_engine = policy_engine or PolicyEngine()
        self.action_executor = action_executor or ActionExecutor(node_id=node_id)
        self.validator = validator or RiskValidator()
        self.telemetry_adapter = telemetry_adapter or TelemetryAdapter()

    def process_raw_telemetry(self, raw: Dict[str, object]) -> PolicyDecision:
        packet = self.telemetry_adapter.from_raw(self.state.node_id, raw)
        return self.process_packet(packet)

    def process_packet(self, packet: TelemetryPacket) -> PolicyDecision:
        signals: List[RiskSignal] = self.validator.derive_signals(packet)
        decision = self.policy_engine.decide(signals)
        context: Dict[str, object] = {"packet": packet, "node_state": {}}
        self.action_executor.execute(decision, context)
        if context["node_state"].get("hardened"):
            self.state.hardened_mode = True
        self.state.last_decision = decision
        return decision
