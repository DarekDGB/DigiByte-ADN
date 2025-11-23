from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ADNConfig:
    """
    Configuration for ADN v2 behaviour.

    These defaults are intentionally conservative and can be tuned by
    DigiByte Core devs, exchanges, miners or Sentinel operators.
    """

    normal_fee_multiplier: float = 1.0
    elevated_fee_multiplier: float = 1.2
    high_fee_multiplier: float = 1.5
    critical_fee_multiplier: float = 2.0

    enable_pqc_on_high: bool = True
    enable_pqc_on_critical: bool = True

    enable_hardened_on_high: bool = True
    enable_hardened_on_critical: bool = True

    global_lock_on_critical: bool = True

    # Risk-score thresholds coming from Sentinel AI v2 + Wallet Guardian
    elevated_threshold: float = 0.35
    high_threshold: float = 0.65
    critical_threshold: float = 0.85

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ADNConfig":
        """
        Lightweight helper for loading from parsed YAML/JSON.
        Unknown keys are ignored.
        """
        allowed = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in allowed}
        return cls(**filtered)
