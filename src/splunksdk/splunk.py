#  pylint: disable=invalid-name
"""Splunk Options."""

from typing import Any, Union

from splunklib.client import KVStoreCollection, Service, KVStoreCollections

from pytoolkit.utilities import flatten_dict

from splunksdk import *


class SplunkApi:
    subclasses: list[str] = []
    _conn: Service

    def __init__(self, **kwargs: Any) -> None:
        self._conn = _splunk_connection(**kwargs)
        subclasses: dict[str, Any] = self._subclass_container()
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

    def __str__(self) -> str:
        return str(self.__class__).split(".")[-1]

    def _subclass_container(self) -> dict[str, Any]:
        _parent_class: SplunkApi = self
        return_object: dict[str, Any] = {}

        class KVstoreWrapper(KVstore):
            def __init__(self) -> None:
                self._parent_class: SplunkApi = _parent_class

        return_object["KVstore"] = KVstoreWrapper

        class SearchWrapper(Search):
            def __init__(self) -> None:
                self._parent_class: SplunkApi = _parent_class

        return_object["Search"] = SearchWrapper
        return return_object


class KVstore:
    """Splunk KVstore
    see: https://docs.splunk.com/Documentation/SplunkCloud/9.0.2305/RESTREF/RESTkvstore
    """

    _parent_class = None
    _collections: list[str]
    _stores: KVStoreCollections
    store: KVStoreCollection
    raw_data: Union[list[dict[str, Any]], None] = None

    def __repr__(self) -> str:
        return f"{self._parent_class.__str__()}.{self.__str__()}"

    def __str__(self) -> str:
        return str(self.__class__).split(".")[-1]

    def set_kvstore(self, collection_name: str) -> None:
        """Sets KVStore Collection."""
        self._set_coll()
        if collection_name not in self._collections:
            raise InvalidNameException(f"Invalid collection name {collection_name}")
        self.store: KVStoreCollection = self.stores[collection_name]

    def _set_coll(self) -> None:
        self._collections = [_.name for _ in self.stores]  # type: ignore

    def get_item(self, key: str) -> dict[str, Any]:
        """Get Item by ID or _key."""
        return self.store.data.query_by_id(id=key)

    def get_collection_data(self, **kwargs: dict[str, Any]) -> None:
        """
        Get collection data.

        :raises NoSuchCapability: _description_
        """
        if not self.store:
            raise NoSuchCapability("Requires a KVstore to be defined")
        # Use standard ops to get filtered resutls
        # Example: s.KVstore.kvstore.data.query(**{"$and":[{"env": {"$eq": "prod"},"isActive":{"$eq": True}}]})
        self.raw_data = self.store.data.query(**kwargs)
        flat: list[dict[str, Any]] = [flatten_dict(_dict) for _dict in self.raw_data]
        # TODO: Build out a recursive yeild that llows for a inline search using exra **params
        # search_results = [data if {} for data in flat]

    def add(self, data):
        self.store.data.insert(data=data)

    def delete(
        self,
    ):
        """Delete entry"""

    def update(self, data) -> None:
        """update entry"""

    def delete_collection(self, collection_name) -> None:
        """Delete Collection"""

    @property
    def collections(self) -> None:
        """Return all avail KVStoreCollections."""
        self._set_coll()

    @property
    def stores(self) -> KVStoreCollections:
        self._stores: KVStoreCollections = self._parent_class._conn.kvstore
        return self._stores


class Search:
    _parent_class = None

    def __repr__(self) -> str:
        return f"{self._parent_class}.{self.__str__()}"

    def __str__(self) -> str:
        return f"Search"
