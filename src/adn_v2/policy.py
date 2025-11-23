from __future__ import annotations

from typing import Iterable, List

from .models import PolicyDecision, RiskLevel, RiskSignal


class PolicyEngine:
    """
    Simple, transparent policy engine for ADN v2.

    It takes a list of RiskSignal objects and returns a single PolicyDecision
    with a chosen RiskLevel and list of actions to execute.
    """

    def __init__(
        self,
        elevated_threshold: float = 0.30,
        high_threshold: float = 0.60,
        critical_threshold: float = 0.85,
    ) -> None:
        self.elevated_threshold = elevated_threshold
        self.high_threshold = high_threshold
        self.critical_threshold = critical_threshold

    def _score(self, signals: Iterable[RiskSignal]) -> float:
        try:
            return max(s.score for s in signals)
        except ValueError:
            return 0.0

    def _level_for_score(self, score: float) -> RiskLevel:
        if score >= self.critical_threshold:
            return RiskLevel.CRITICAL
        if score >= self.high_threshold:
            return RiskLevel.HIGH
        if score >= self.elevated_threshold:
            return RiskLevel.ELEVATED
        return RiskLevel.NORMAL

    def _actions_for_level(self, level: RiskLevel) -> List[str]:
        if level is RiskLevel.NORMAL:
            return ["log"]
        if level is RiskLevel.ELEVATED:
            return ["log", "alert"]
        if level is RiskLevel.HIGH:
            return ["log", "alert", "harden_node", "isolate_peers"]
        return [
            "log",
            "alert",
            "harden_node",
            "isolate_peers",
            "throttle_mempool",
            "notify_wallet_guardian",
        ]

    def decide(self, signals: List[RiskSignal]) -> PolicyDecision:
        if not signals:
            return PolicyDecision(
                level=RiskLevel.NORMAL,
                score=0.0,
                reason="no signals",
                actions=["log"],
            )

        score = self._score(signals)
        level = self._level_for_score(score)
        reason = ", ".join(f"{s.source}:{s.score:.2f}" for s in signals)
        actions = self._actions_for_level(level)

        return PolicyDecision(
            level=level,
            score=score,
            reason=reason,
            actions=actions,
        )
