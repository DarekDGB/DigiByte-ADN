from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .v3_reason_codes import ReasonCode


_ALLOWED_TOP_LEVEL_KEYS = {"contract_version", "component", "request_id", "events"}


def _contains_bad_number(x: Any) -> bool:
    """
    Fail-closed numeric validation.
    Reject NaN/Infinity anywhere in the request.
    """
    if isinstance(x, float):
        # NaN != NaN, infinities compare like this:
        if x != x:
            return True
        if x == float("inf") or x == float("-inf"):
            return True
        return False
    if isinstance(x, dict):
        return any(_contains_bad_number(v) for v in x.values())
    if isinstance(x, list):
        return any(_contains_bad_number(v) for v in x)
    return False


@dataclass(frozen=True)
class ADNv3Request:
    contract_version: int
    component: str
    request_id: str
    events: List[Dict[str, Any]]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ADNv3Request":
        if not isinstance(d, dict):
            raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)

        # strict unknown key rejection
        unknown = set(d.keys()) - _ALLOWED_TOP_LEVEL_KEYS
        if unknown:
            raise ValueError(ReasonCode.ADN_ERROR_UNKNOWN_KEY.value)

        if _contains_bad_number(d):
            raise ValueError(ReasonCode.ADN_ERROR_BAD_NUMBER.value)

        contract_version = d.get("contract_version", None)
        component = d.get("component", None)
        request_id = d.get("request_id", None)
        events = d.get("events", None)

        if not isinstance(contract_version, int):
            raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)
        if not isinstance(component, str) or not component.strip():
            raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)
        if not isinstance(events, list):
            raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)

        # events must be list of dicts (for now)
        for e in events:
            if not isinstance(e, dict):
                raise ValueError(ReasonCode.ADN_ERROR_INVALID_REQUEST.value)

        return cls(
            contract_version=contract_version,
            component=component.strip(),
            request_id=request_id.strip(),
            events=events,
        )
