"""Splunk Options."""

from typing import Any, Optional, Union

from splunklib.client import KVStoreCollection, Service, KVStoreCollections

from pytoolkit.utilities import flatten_dict

from splunksdk import *
from splunksdk.utils.statics import KVSTORE_QUERY


class SplunkApi:

    subclasses = []
    _conn: Optional[Service]

    def __init__(self, **kwargs: Any):
        self._conn = _splunk_connection(**kwargs)
        subclasses: dict[str, Any] = self._subclass_container()
        self.subclasses = list(subclasses)
        self.KVstore: Any = subclasses["KVstore"]()
        self.Search: Any = subclasses["Search"]()

    def _add_subclass(self, subclass):
        self.subclasses.append(subclass)

    @property
    def conn(self) -> Service:
        return self._conn

    def _subclass_container(self):
        _parent_class: SplunkApi = self
        return_object: dict[str, Any] = {}

        class KVstoreWrapper(KVstore):
            def __init__(self) -> None:
                self._parent_class = _parent_class
        return_object["KVstore"] = KVstoreWrapper

        class SearchWrapper(Search):
            def __init__(self) -> None:
                self._parent_class = _parent_class
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
        return f"{self._parent_class}.{self.__str__()}"

    def __str__(self) -> str:
        return f"{self.__class__}"

    def set_kvstore(self, collection_name: str):
        """Sets KVStore Collection."""
        self._set_coll()
        if collection_name not in self._collections:
            raise InvalidNameException(
                f"Invalid collection name {collection_name}")
        self.store: KVStoreCollection = self.stores[collection_name]

    def _set_coll(self):
        self._collections = [_.name for _ in self.stores]  # type: ignore

    def get_item(self, key: str) -> dict[str, Any]:
        """Get Item by ID or _key."""
        return self.store.data.query_by_id(id=key)

    def get_collection_data(self, **kwargs: dict[str, Any]):
        """
        Get collection data.

        :raises NoSuchCapability: _description_
        """
        if not self.store:
            raise NoSuchCapability("Requires a KVstore to be defined")
        # Use standard ops to get filtered resutls
        # Example: s.KVstore.kvstore.data.query(**{"$and":[{"env": {"$eq": "prod"},"isActive":{"$eq": True}}]})
        self.raw_data = self.store.data.query(**kwargs)
        flat = [flatten_dict(_dict) for _dict in self.raw_data]
        # TODO: Build out a recursive yeild that llows for a inline search using exra **params
        # search_results = [data if {} for data in flat]

    def add(self, data):
        self.store.data.insert(data=data)

    def delete(self,):
        """Delete entry"""

    def update(self, data):
        """update entry"""

    def delete_collection(self, collection_name):
        """Delete Collection"""

    @property
    def collections(self):
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
        return f"{self.__class__}"
