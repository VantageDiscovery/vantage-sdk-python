# coding: utf-8

"""
    Vantage API

    This is a the API to interact with Vantage Discovery, the amazing Semantic Search Platform in the world.  We enable developers to build magical discovery experiences into their products and websites.  Some useful links: - [TODO: Semantic Search Guide: What Is It And Why Does It Matter?](https://www.bloomreach.com/en/blog/2019/semantic-search-explained-in-5-minutes)

    The version of the OpenAPI document: v1.1.2
    Contact: devrel@vantagediscovery.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Union

from pydantic import BaseModel, StrictFloat, StrictInt

from vantage.core.http.models.global_search_properties_collection import (
    GlobalSearchPropertiesCollection,
)
from vantage.core.http.models.global_search_properties_filter import (
    GlobalSearchPropertiesFilter,
)
from vantage.core.http.models.global_search_properties_pagination import (
    GlobalSearchPropertiesPagination,
)
from vantage.core.http.models.global_search_properties_sort import (
    GlobalSearchPropertiesSort,
)


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class EmbeddingSearchQuery(BaseModel):
    """
    EmbeddingSearchQuery
    """  # noqa: E501

    collection: Optional[GlobalSearchPropertiesCollection] = None
    request_id: Optional[StrictInt] = None
    filter: Optional[GlobalSearchPropertiesFilter] = None
    pagination: Optional[GlobalSearchPropertiesPagination] = None
    sort: Optional[GlobalSearchPropertiesSort] = None
    embedding: Optional[List[Union[StrictFloat, StrictInt]]] = None
    __properties: ClassVar[List[str]] = [
        "collection",
        "request_id",
        "filter",
        "pagination",
        "sort",
        "embedding",
    ]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of EmbeddingSearchQuery from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of collection
        if self.collection:
            _dict['collection'] = self.collection.to_dict()
        # override the default output from pydantic by calling `to_dict()` of filter
        if self.filter:
            _dict['filter'] = self.filter.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sort
        if self.sort:
            _dict['sort'] = self.sort.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of EmbeddingSearchQuery from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "collection": GlobalSearchPropertiesCollection.from_dict(
                    obj.get("collection")
                )
                if obj.get("collection") is not None
                else None,
                "request_id": obj.get("request_id"),
                "filter": GlobalSearchPropertiesFilter.from_dict(
                    obj.get("filter")
                )
                if obj.get("filter") is not None
                else None,
                "pagination": GlobalSearchPropertiesPagination.from_dict(
                    obj.get("pagination")
                )
                if obj.get("pagination") is not None
                else None,
                "sort": GlobalSearchPropertiesSort.from_dict(obj.get("sort"))
                if obj.get("sort") is not None
                else None,
                "embedding": obj.get("embedding"),
            }
        )
        return _obj
