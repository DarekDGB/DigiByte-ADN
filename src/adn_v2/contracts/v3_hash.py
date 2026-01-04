from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def canonical_sha256(payload: Dict[str, Any]) -> str:
    """
    Deterministic hash of a JSON-like payload.
    - stable key ordering
    - stable separators
    - UTF-8 encoding
    """
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
