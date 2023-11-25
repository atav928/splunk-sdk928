"""Initialization."""

from splunksdk.utils.configs import Config
from splunksdk._version import __version__

APP_LIST: list[str] = ["appname", "splunkapp", "app"]

config = Config()

try:
    from splunklib.client import (
        IllegalOperationException,
        IncomparableException,
        AmbiguousReferenceException,
        InvalidNameException,
        NoSuchCapability,
        OperationError,
        NotSupportedError,
    )
    # Aditional Exceptions

    class SplunkApiNoOperationRunning(OperationError):
        """SplunkAPI Customized Operation Error Exception."""
    class SplunkSearchError(OperationError):
        """SplunkAPI Customized Search Results Returned Error Message."""
    class SplunkSearchFatal(OperationError):
        """SplunkAPI Fatal Error in Search."""
except ImportError:
    pass

__all__: list[str] = [
    "IllegalOperationException",
    "IncomparableException",
    "AmbiguousReferenceException",
    "InvalidNameException",
    "NoSuchCapability",
    "OperationError",
    "NotSupportedError",
    "SplunkApiNoOperationRunning",
    "SplunkSearchError",
    "SplunkSearchFatal",
]
