"""Async Python client for Besen BS20 EV chargers."""

from __future__ import annotations

from .client import BesenBS20Client
from .exceptions import (
    BesenBS20Error,
    CannotConnect,
    CommandFailed,
    InvalidAuth,
    NoConnectablePath,
    ProtocolError,
)
from .models import (
    BesenBS20Data,
    BoardRevision,
    CharacteristicPair,
    ChargerConfig,
    ChargerInfo,
    ChargeStatus,
    CommandResult,
)

__version__ = "0.2.2"

__all__ = [
    "BesenBS20Client",
    "BesenBS20Data",
    "BesenBS20Error",
    "BoardRevision",
    "CannotConnect",
    "CharacteristicPair",
    "ChargeStatus",
    "ChargerConfig",
    "ChargerInfo",
    "CommandFailed",
    "CommandResult",
    "InvalidAuth",
    "NoConnectablePath",
    "ProtocolError",
]
