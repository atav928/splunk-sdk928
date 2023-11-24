#  pylint: disable=invalid-name,wildcard-import,unused-wildcard-import,protected-access,undefined-variable,too-few-public-methods,unsubscriptable-object
"""Splunk Options."""

from typing import Any, Union, Dict

from splunklib.data import Record
from splunklib.client import KVStoreCollection, Service, KVStoreCollections

from pytoolkit.utilities import flatten_dict

from splunksdk import *


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
    _collections: list[str]
    _stores: KVStoreCollections
    store: KVStoreCollection
    raw_data: Union[list[Dict[str, Any]], None] = None

    def __repr__(self) -> str:
        """Class Representation."""
        return f"{self._parent_class.__str__()}.{self.__str__()}"

    def __str__(self) -> str:
        """String Representation of Class."""
        return str(self.__class__).split(".", maxsplit=-1)[-1]

    def set_kvstore(self, collection_name: str) -> None:
        """Sets KVStore Collection."""
        self._check_collection(collection_name)
        self.store: KVStoreCollection = self.stores[collection_name]

    def _set_coll(self) -> None:
        self._collections = [_.name for _ in self.stores]  # type: ignore

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
        #flat: list[Dict[str, Any]] = [
        #    flatten_dict(_dict) for _dict in self.raw_data]
        # TODO: Build out a recursive yeild that llows for a inline search using exra **params
        # search_results = [data if {} for data in flat]

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
        coll_return: Record = self.stores.create(name=name, **kwargs)  # type: ignore
        if coll_return.get("status") != 201:
            raise OperationError(f"Unable to create collection {name}")
        self.set_kvstore(collection_name=name)

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
        coll_insert: Dict[str, Any] = self.store.data.insert(data=data)  # type: ignore
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
        self._check_collection(collection_name)
        self.set_kvstore(collection_name=collection_name)
        self.store.delete()

    def _check_collection(self, name: str) -> None:
        self._set_coll()
        if name in self._collections:
            raise InvalidNameException(f"Collection already exists {name}")

    @property
    def collections(self) -> None:
        """Return all avail KVStoreCollections."""
        self._set_coll()

    @property
    def stores(self) -> KVStoreCollections:
        """KVStoreCollections."""
        self._stores: KVStoreCollections = self._parent_class._conn.kvstore
        return self._stores  # type: ignore


class Search:
    """Splunk Search."""

    _parent_class = None

    def __repr__(self) -> str:
        """Class Representation."""
        return f"{self._parent_class.__str__()}.{self.__str__()}"

    def __str__(self) -> str:
        """String Representation of Class."""
        return str(self.__class__).split(".", maxsplit=-1)[-1]
