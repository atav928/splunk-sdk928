"""Utilities."""

import json
import tempfile
from typing import Any, List
import uuid

import pandas as pd
from pandas import DataFrame
from splunklib.results import JSONResultsReader

from pytoolkit.utilities import flatten_dict, nested_dict
from pytoolkit.py_cert.cacert import castore_custom_delete

from splunksdk.utils.search import SplunkSearchResults

# TODO: replace with other functions in pytoolkit
def get_tempdir() -> str:
    """Returns tempdir"""
    return tempfile.gettempdir()

def splunk_temp(extension: str) -> str:
    """Temp splunk file for search."""
    return f"{get_tempdir()}/splunk_{Utils.uuid()}.{extension}"



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

    @classmethod
    def to_csv(cls, **kwargs: Any) -> DataFrame:
        """Convert Response to CSV DataFrame."""
        try:
            # If sending in as a CSV Ensure that the type of Dictionary is flattened.
            return pd.read_csv(kwargs["service"])
        except KeyError:
            return pd.DataFrame.from_records(kwargs["data"],index='_key')

    @classmethod
    def to_xml(cls, **kwargs: Any) -> List[Any]:
        """Convert Resonse to XML list."""
        filename = splunk_temp(extension="xml")
        with open(filename, 'wb') as f:
            f.writelines(kwargs["service"])
        with open(filename,'rb') as f:
            values = f.readlines()
        castore_custom_delete(filename)
        return values

    @classmethod
    def to_json(cls, **kwargs: Any) -> list[dict[str, Any]]:
        """Convert JSON_COLS and JSON_ROWS to JSON Objects."""
        filename = splunk_temp(extension='json')
        with open(filename,'wb') as f:
            f.writelines(kwargs["service"])
        with open(filename,'rb') as f:
            values = json.load(f)
        castore_custom_delete(filename)
        return values

    @staticmethod
    def splunk_exporter(**kwargs: Any) -> SplunkSearchResults:
        """
        Export Splunk Records and reformat into a dictionary.

        :return: _description_
        :rtype: list[dict[str, Any]]
        """
        results = JSONResultsReader(kwargs["service"])
        # TODO: Convert to a dataclass object that can also hold the metadata or use python pipe
        # https://towardsdatascience.com/write-clean-python-code-using-pipes-1239a0f3abf5
        message: dict[str, Any] = {}
        json_results = [_ if isinstance(_, dict) else message.update({str(_.type): str(_.message)}) for _ in results]
        return SplunkSearchResults(message=message, json_response=json_results)
