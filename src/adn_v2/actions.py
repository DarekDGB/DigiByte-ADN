from __future__ import annotations

from .models import DefenseDecision


class ActionExecutor:
    """
    Thin abstraction around 'real' node / infra actions.

    In this reference skeleton it only logs intent.
    DigiByte Core or infra scripts will plug real behaviour here.
    """

    def apply(self, decision: DefenseDecision) -> None:
        # In the reference skeleton we do nothing dangerous.
        # Real implementations would call RPC, adjust config, etc.
        print("[ADN v2] Applying decision:", decision)
