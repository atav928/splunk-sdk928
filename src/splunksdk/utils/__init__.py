"""Utilities."""

import uuid

class Utils:
    """Utilities for Internal Usage."""

    @staticmethod
    def uuid(appname: str = "", to_hex: bool = True) -> str:
        """
        Creates a UUID that can be used as a unique ID value.

        :param appname: appname, defaults to ""
        :type appname: str, optional
        :param to_hex: _description_, defaults to True
        :type to_hex: bool, optional
        :return: ID
        :rtype: str
        """
        _id: str = uuid.uuid4().hex if to_hex else str(uuid.uuid4())
        return f'{appname.replace(" ","_")}:{_id}' if appname else _id
