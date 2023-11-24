"""Initialization."""
from typing import Any

from splunksdk.utils.configs import Config
from splunksdk.utils.login import SplunkLogin
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
    "_splunk_connection",
]


def _splunk_connection(**kwargs: Any):
    """
    This function connects and logs in to a Splunk instance.

    This function is a shorthand for :meth:`Service.login`.
    The ``connect`` function makes one round trip to the server (for logging in).

    See ``SplunkLogin`` Dataclass for details.

    **Example**::

        import splunklib.client as client
        s = client.connect(...)
        a = s.apps["my_app"]
        ...
    """
    import splunklib.client as sp_client  # pylint: disable=import-outside-toplevel
    if "host" not in kwargs:
        kwargs["host"] = kwargs.get("splunk_host",kwargs.get("hostname","localhost"))
    return sp_client.connect(  # type: ignore
        **SplunkLogin.create_from_kwargs(**kwargs).to_dict()
    )
