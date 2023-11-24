# pylint: disable=invalid-name,too-many-instance-attributes
"""Splunk Login Dataclass Structure."""

from typing import Union, Optional

from ssl import SSLContext
from dataclasses import dataclass

from pytoolkit.utilities import BaseMonitor, NONETYPE
from pytoolkit.utils import set_bool

SHARING: list[str] = ["global", "system", "app", "user"]

@dataclass
class SplunkLogin(BaseMonitor):
    """Dataclass Variables used to connect to Splunk Instance.

    :param host: The host name (the default is "localhost").
    :type host: ``string``
    :param port: The port number (the default is 8089).
    :type port: ``integer``
    :param scheme: The scheme for accessing the service (the default is "https").
    :type scheme: "https" or "http"
    :param verify: Enable (True) or disable (False) SSL verification for
                    https connections. (optional, the default is True)
    :type verify: ``Boolean``
    :param `owner`: The owner context of the namespace (optional).
    :type owner: ``string``
    :param `app`: The app context of the namespace (optional).
    :type app: ``string``
    :param sharing: The sharing mode for the namespace (the default is "user").
    :type sharing: "global", "system", "app", or "user"
    :param `token`: The current session token (optional). Session tokens can be
                    shared across multiple service instances.SSL
    :type token: ``string``
    :param cookie: A session cookie. When provided, you don't need to call :meth:`login`.
        This parameter is only supported for Splunk 6.2+.
    :type cookie: ``string``
    :param autologin: When ``True``, automatically tries to log in again if the
        session terminates.
    :type autologin: ``boolean``
    :param `username`: The Splunk account username, which is used to
                        authenticate the Splunk instance.
    :type username: ``string``
    :param `password`: The password for the Splunk account.
    :type password: ``string``
    :param retires: Number of retries for each HTTP connection (optional, the default is 0).
                    NOTE THAT THIS MAY INCREASE THE NUMBER OF ROUND TRIP CONNECTIONS TO THE SPLUNK SERVER.
    :type retries: ``int``
    :param retryDelay: How long to wait between connection attempts if `retries` > 0 (optional, defaults to 10s).
    :type retryDelay: ``int`` (in seconds)
    :param `context`: The SSLContext that can be used when setting verify=True (optional)
    :type context: ``SSLContext``
    :return: An initialized :class:`Service` connection.

    **Example**::

        import splunklib.client as client
        s = client.connect(...)
        a = s.apps["my_app"]
        ...
    """
    password: str
    host: str
    username: str
    port: int = 8089
    scheme: str = "https"
    verify: Union[str, bool] = True
    owner: Optional[str] = NONETYPE
    app: Optional[str] = NONETYPE
    sharing: str = "user"
    token: Optional[str] = NONETYPE
    cookie: Optional[str] = NONETYPE
    autologin: Optional[bool] = False
    retries: int = 0
    retryDelay: int = 10
    context: Optional[SSLContext] = NONETYPE

    def __post_init__(self):
        if self.sharing not in SHARING:
                raise ValueError(f"Invalid param sharing {self.sharing}")
        self.verify: Union[str, bool]= set_bool(value=self.verify) # type: ignore
