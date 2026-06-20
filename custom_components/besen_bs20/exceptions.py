"""Exceptions raised by the Besen BS20 integration."""


class BesenBS20Error(Exception):
    """Base class for Besen BS20 errors."""


class CannotConnect(BesenBS20Error):
    """Raised when the charger cannot be reached."""


class InvalidAuth(BesenBS20Error):
    """Raised when the charger rejects the PIN."""


class ProtocolError(BesenBS20Error):
    """Raised when charger data is malformed."""


class CommandFailed(BesenBS20Error):
    """Raised when a charger command fails."""
