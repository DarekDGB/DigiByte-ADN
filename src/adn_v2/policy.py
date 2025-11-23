"""
ADN v2 Policy Engine (placeholder)

This minimal version exists so imports succeed during CI testing.
Full implementation will be added soon.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PolicyDecision:
    allow: bool
    reason: str
    level: str = "normal"


class PolicyEngine:
    def __init__(self):
        self.rules = {}

    def evaluate(self, telemetry: Dict[str, Any]) -> PolicyDecision:
        """
        Minimal placeholder evaluation.
        Returns a safe default decision.
        """
        return PolicyDecision(
            allow=True,
            reason="placeholder-policy-engine",
            level="normal"
        )
