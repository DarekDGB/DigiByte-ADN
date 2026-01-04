from __future__ import annotations

from enum import Enum


class ReasonCode(str, Enum):
    # success / neutral
    ADN_OK = "ADN_OK"

    # fail-closed contract errors
    ADN_ERROR_INVALID_REQUEST = "ADN_ERROR_INVALID_REQUEST"
    ADN_ERROR_SCHEMA_VERSION = "ADN_ERROR_SCHEMA_VERSION"
    ADN_ERROR_UNKNOWN_KEY = "ADN_ERROR_UNKNOWN_KEY"
    ADN_ERROR_BAD_NUMBER = "ADN_ERROR_BAD_NUMBER"
