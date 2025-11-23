from __future__ import annotations

from typing import Iterable

from .config import ADNConfig, load_default_config
from .models import (
    ChainSnapshot,
    SentinelSignal,
    GuardianSignal,
    DefenseDecision,
)
from .policy import DefensePolicy
from .actions import ActionExecutor


class ADNEngine:
    """
    Core ADN v2 orchestration engine.

    1. Takes structured objects from Sentinel & Wallet Guardian
    2. Uses DefensePolicy to decide final risk level
    3. Hands the decision to ActionExecutor
    """

    def __init__(
        self,
        config: ADNConfig | None = None,
        executor: ActionExecutor | None = None,
    ) -> None:
        self.config = config or load_default_config()
        self.policy = DefensePolicy(self.config)
        self.executor = executor or ActionExecutor()

    def evaluate_and_apply(
        self,
        chain: ChainSnapshot,
        sentinel: SentinelSignal,
        guardians: Iterable[GuardianSignal],
    ) -> DefenseDecision:
        decision = self.policy.decide(chain, sentinel, guardians)
        self.executor.apply(decision)
        return decision
