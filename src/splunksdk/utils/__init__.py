"""Utilities."""

from typing import Any
import uuid

import pandas as pd
from pandas import DataFrame

from pytoolkit.utilities import flatten_dict, nested_dict

class Utils:
    """Utilities for Internal Usage."""

    dataframe: DataFrame

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

    def import_csv(self, filename: str, **kwargs: Any) -> None:
        """Import CSV to DataFrame."""
        self._set_data(pd.read_csv(filename, **kwargs))

    def convert_to_dataframe(self):
        """Convert DF."""

    def _set_data(self, data: DataFrame) -> None:
        self.dataframe = data
