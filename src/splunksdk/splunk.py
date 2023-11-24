#  pylint: disable=invalid-name,wildcard-import,unused-wildcard-import,protected-access,undefined-variable,too-few-public-methods,unsubscriptable-object
"""Splunk Options."""

import tempfile
from typing import Any, Union, Dict, List
from pandas import DataFrame


from splunklib import results as sp_results

from splunklib.data import Record
from splunklib.client import KVStoreCollection, Service, KVStoreCollections, Jobs, Job

from pytoolkit.utilities import flatten_dict, nested_dict
from pytoolkit.utils import reformat_exception

from splunksdk import *
from splunksdk.utils.statics import SPLUNK_OUTPUTMODES
from splunksdk.utils.kvstore import Collections
from splunksdk.utils import Utils


class SplunkApi:
    """Splunk API."""

    _conn: Service
    subclasses: list[str] = []

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize Splunk API.
        """
        self._conn = _splunk_connection(**kwargs)
        subclasses: Dict[str, Any] = self._subclass_container()
        self.subclasses = list(subclasses)
        self.KVstore: Any = subclasses["KVstore"]()
        self.Search: Any = subclasses["Search"]()

    @property
    def conn(self) -> Service:
        """Splunk Service Connection.

        :return: Splunk Connection
        :rtype: Service
        """
        return self._conn

    def __repr__(self) -> str:
        """Class Representation."""
        return self.__str__()

    def __str__(self) -> str:
        """String Representation of Class."""
        return str(self.__class__).split(".", maxsplit=-1)[-1]

    def _subclass_container(self) -> Dict[str, Any]:
        _parent_class: SplunkApi = self
        return_object: Dict[str, Any] = {}

        class KVstoreWrapper(KVstore):
            """KVStoreWrapper"""

            def __init__(self) -> None:
                self._parent_class: SplunkApi = _parent_class

        return_object["KVstore"] = KVstoreWrapper

        class SearchWrapper(Search):
            """SearchWrapper"""

            def __init__(self) -> None:
                self._parent_class: SplunkApi = _parent_class

        return_object["Search"] = SearchWrapper
        return return_object


class KVstore:
    """
    Splunk KVstore
    see: https://docs.splunk.com/Documentation/SplunkCloud/9.0.2305/RESTREF/RESTkvstore
    """

    _parent_class = None
    _stores: KVStoreCollections
    _collections: List[str]
    store: KVStoreCollection
    raw_data: Union[list[Dict[str, Any]], None] = None
    flat_data: Union[list[Dict[str, Any]], None] = None
    nested_data: Union[list[Dict[str, Any]], None] = None

    #TODO: Figure out hwo to handle colllections as a property or as something else as getting attribute errors
    def __repr__(self) -> str:
        """Class Representation."""
        return f"{self._parent_class.__str__()}.{self.__str__()}"

    def __str__(self) -> str:
        """String Representation of Class."""
        return str(self.__class__).split(".", maxsplit=-1)[-1]

    def set_kvstore(self, collection_name: str) -> None:
        """Sets KVStore Collection."""
        self._collection_not_exists(collection_name)
        self.store: KVStoreCollection = self.stores[collection_name]

    #def _set_coll(self) -> None:
    #    self.collections = [_.name for _ in self.stores]  # type: ignore

    @property
    def collections(self) -> List[str]:
        setattr(self,"_collections",[_.name for _ in self.stores])# type: ignore
        return self._collections
    
    def get_item(self, key: str) -> Dict[str, Any]:
        """Get Item by ID or _key."""
        return self.store.data.query_by_id(id=key)

    def get_collection_data(self, **kwargs: Dict[str, Any]) -> None:
        """
        Get collection data.

        :raises NoSuchCapability: _description_
        """
        if not self.store:
            raise NoSuchCapability("Requires a KVstore to be defined")
        # Use standard ops to get filtered resutls
        # Example: s.KVstore.kvstore.data.query(**{"$and":[{"env": {"$eq": "prod"},"isActive":{"$eq": True}}]})
        self.raw_data = self.store.data.query(**kwargs)
        self.flat_data = [flatten_dict(_dict) for _dict in self.raw_data]
        self.nested_data = [nested_dict(_dict) for _dict in self.raw_data]
        # TODO: Build out a recursive yeild that llows for a inline search using exra **params
        # search_results = [data if {} for data in flat]

    def to_csv(self) -> Union[DataFrame,None]:
        """
        Returns a Dataframe formated into a CSV format.

        :return: _description_
        :rtype: Union[DataFrame,None]
        """
        if self.flat_data:
            return Utils.to_csv(data=self.flat_data)

    def _add_collection(self, name: str) -> None:
        self._collections.append(name)
    
    def _del_collection(self, name: str) -> None:
        self._collections.remove(name)

    def create_collection(self, name: str, **kwargs: Dict[str, Any]) -> None:
        """
        Creates a KV Store Collection.

        :param name: name of collection to create
        :type name: ``string``
        :param accelerated_fields: dictionary of accelerated_fields definitions
        :type accelerated_fields: ``dict``
        :param fields: dictionary of field definitions
        :type fields: ``dict``
        :param kwargs: a dictionary of additional parameters specifying indexes and field definitions
        :type kwargs: ``dict``

        :return: Result of POST request
        """
        self._collection_exists(name=name)
        coll_return: Record = self.stores.create(name=name, **kwargs)  # type: ignore
        if coll_return.get("status") != 201:
            raise OperationError(f"Unable to create collection {name}")
        self.set_kvstore(collection_name=name)
        self._add_collection(name=name)

    def insert_data(self, data: Union[str, Dict[str, Any]]) -> None:
        """
        Inserts item into this collection. An _id field will be generated if not assigned in the data.

        :param data: Document to insert
        :type data: ``string`` or ``dict``

        :raises NoSuchCapability: _description_
        :raises OperationError: _description_
        """
        if not self.store:
            raise NoSuchCapability("KVStoreCollection not defined")
        coll_insert: Dict[str, Any] = self.store.data.insert(
            data=data)  # type: ignore
        if not coll_insert.get("_key"):
            raise OperationError(f"Unable to insert data {data}")

    def delete_data(self) -> None:
        """Delete entry"""

    def update_data(self, key: str, data: Union[Dict[str, Any], str]) -> None:
        """update entry"""
        if not self.store and self.store.data.query_by_id(key):
            raise OperationError(f"Missing Collection or invalid _key {key}")
        self.store.data.update(id=key, data=data)

    def delete_collection(self, collection_name: str) -> None:
        """
        Delete Collection.
        """
        self._collection_not_exists(collection_name)
        self.set_kvstore(collection_name=collection_name)
        self.store.delete()
        self._del_collection(name=collection_name)

    def _collection_exists(self, name: str) -> None:
        #self._set_coll()
        if name in self.collections:
            raise InvalidNameException(f"Collection already exists {name}")
        
    def _collection_not_exists(self, name: str) -> None:
        #self._set_coll()
        if name not in self.collections:
            raise InvalidNameException(f"Collection does not exists {name}")

    @property
    def stores(self) -> KVStoreCollections:
        """KVStoreCollections."""
        self._stores: KVStoreCollections = self._parent_class._conn.kvstore  # type: ignore
        return self._stores  # type: ignore


class Search:
    """Splunk Search."""

    _parent_class = None
    _output_mode: str = "json"
    json_results: dict[str, Any]
    csv_results: DataFrame
    json_cols_results: dict[str, Any]
    json_rows_results: dict[str, Any]
    xml_results: list[Any]
    job: Job
    raw_results: Any
    search_query: Union[str, None] = None

    def __repr__(self) -> str:
        """Class Representation."""
        return f"{self._parent_class.__str__()}.{self.__str__()}"

    def __str__(self) -> str:
        """String Representation of Class."""
        return str(self.__class__).split(".", maxsplit=-1)[-1]

    @property
    def jobs(self) -> Jobs:
        self._jobs = self._parent_class._conn.jobs  # type: ignore
        return self._jobs  # type: ignore

    @property
    def output_mode(self) -> str:
        return self._output_mode

    @output_mode.setter
    def output_mode(self, value: str) -> None:
        if value.lower() not in SPLUNK_OUTPUTMODES:
            raise InvalidNameException(f"Invalid output mode {value}")
        self._output_mode = value.lower()

    def add_query(self, search_query: str, **kwargs: Union[str, dict[str, Any]]) -> None:
        self.search_query = search_query

    def start_search(self, **kwargs: Any):
        # create a job
        try:
            if not self.search_query:
                self.add_query(search_query=kwargs.pop("query") if kwargs.get("query") else kwargs.get("search_query"))
        except:
            raise OperationError("Unable to run search without a search query")
        self.job: Job= self.jobs.create(query=self.search_query, **kwargs)

    def get_results(self, **kwargs: Any) -> bool:
        """
        Generates reults once completed into file format that is permitted.

        :raises InvalidNameException: _description_
        :return: _description_
        :rtype: Any
        """
        try:
            if self.job.is_done():
                if kwargs.get("output_mode"):
                    self._output_mode = kwargs.pop("output_mode")
                self.csv_results = Utils.to_csv(service=self.job.results(output_mode='csv'))
                self.raw_results = self.job.results
                self.json_results = Utils.splunk_exporter(service=self.job.results(output_mode="json"))
                self.json_cols_results = Utils.to_json(service=self.job.results(output_mode="json_cols"),output_mode="json_cols")
                self.json_rows_results = Utils.to_json(service=self.job.results(output_mode="json_rows"),output_mode="json_rows")
                self.xml_results = Utils.to_xml(service=self.job.results(output_mode="xml"),output_mode="xml")
                return self.job.is_done()
            return False
        except Exception as err:
            error: str = reformat_exception(err)
            raise InvalidNameException(error)
    
    def print_results(self, location: str, output_mode: str = "json") -> str:
        """
        Print out file based on location specified.

        :param location: _description_
        :type location: str
        :param output_mode: _description_, defaults to "json"
        :type output_mode: str, optional
        """
        extension: str = output_mode.split('_')[0]
        filename: str = f"{location}/results_sid_{self.job.sid}.{extension}"
        with open(filename,'wb') as f:
            f.writelines(self.job.results(output_mode=output_mode))
        return filename

    def cancel_job(self) -> None:
        """Cancel current job."""
        self.job.cancel()
