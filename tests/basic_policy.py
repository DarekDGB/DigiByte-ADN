"""
Basic structural tests for DigiByte-ADN-v2.

Goal:
- Prove that core config + engine modules import correctly.
- Keep tests very simple so they pass reliably on CI.
"""

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    """
    Ensure the `src` directory is on sys.path so that `adn_v2`
    can be imported when GitHub Actions runs pytest.
    """
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


# Make sure src/ is visible **before** we import adn_v2.*
_ensure_src_on_path()

import adn_v2.config as config
import adn_v2.engine as engine


def test_default_config_exists() -> None:
    """The default ADN config should be defined."""
    assert hasattr(config, "DEFAULT_ADN_CONFIG")


def test_engine_class_exists() -> None:
    """The ADNEngine class should be available."""
    assert hasattr(engine, "ADNEngine")
