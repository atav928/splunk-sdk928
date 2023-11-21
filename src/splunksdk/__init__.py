"""Initialization."""
from typing import Any

from splunksdk.utils.configs import Config
from splunksdk._version import __version__

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

__all__ = [
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
    Splunk basic connection meant to be used throughout project.

    :return: _description_
    :rtype: _type_
    """
    import splunklib.client as sp_client  # pylint: disable=import-outside-toplevel
    APP_LIST = ["appname", "splunkapp", "app"]
    app = ""
    for _ in APP_LIST:
        if kwargs.get(_):
            app = kwargs[_]
            break
    return sp_client.connect(
            host=kwargs.get("splunk_host",kwargs["host"]),
            username=kwargs["username"],
            port=kwargs.get("mgmtport", kwargs["port"]),
            password=kwargs["password"],
            app=app,
            owner=kwargs["owner"],
            sharing=kwargs["sharing"]
    )
