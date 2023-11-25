# pylint: disable=too-few-public-methods
"""Configurations."""


class Config:
    """Splunk Configurations."""
    LOGNAME: str = "splunk.log"
    LOGSTREAM: bool = False
    LOGDIR: str = ""
    LOGLEVEL: str = "INFO"
    SETLOG: bool = True
    SETFILE: bool = True
    YAML_CONFIG: str = ""
