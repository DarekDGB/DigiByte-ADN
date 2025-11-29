"""
ADN v2 – Configuration Module
Central configuration for thresholds, modes and network parameters.
"""

ADN_VERSION = "2.0.0"

# --- RISK THRESHOLDS -------------------------------------------------------

BASELINE_THRESHOLDS = {
    "low": 0.25,        # harmless anomalies
    "elevated": 0.45,   # unusual behaviour
    "high": 0.70,       # requires human confirmation
    "critical": 0.90    # automatic defensive action
}

# --- HARDENED MODE PARAMETERS ----------------------------------------------

HARDENED_MODE = {
    "enabled": True,
    "min_peer_score": 0.65,          # drop peers below this trust score
    "max_reorg_depth": 2,           # reject reorgs deeper than 2 blocks
    "fee_multiplier": 1.5,          # temporary fee boost for spam defence
}

# --- TELEMETRY --------------------------------------------------------------

TELEMETRY = {
    "enabled": True,
    "remote_endpoint": "https://defense.dgb/adn-telemetry",
    "interval_seconds": 30,
}

# --- POLICY ENGINE ----------------------------------------------------------

POLICY = {
    "reject_unknown_script": True,
    "block_rbf_high_risk": True,
    "freeze_unknown_peers": True,
}

# --- v2 compatibility shim ----------------------------------------------------
# Older parts of ADN v2 (e.g. validator) expect an ADNConfig object.
# We provide a minimal, backwards-compatible version here so imports succeed.

from dataclasses import dataclass


@dataclass
class ADNConfig:
    """
    Minimal configuration object for legacy validator / policy code.

    Newer v2 defense logic uses NodeDefenseConfig from models.py instead,
    but we keep this class so older integrations and tests still import
    `ADNConfig` without errors.
    """
    enabled: bool = True
    name: str = "default"
    notes: str = ""
