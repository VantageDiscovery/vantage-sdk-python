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
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, StrictInt, StrictStr

from vantage_sdk.core.http.models.search_options_collection import (
    SearchOptionsCollection,
)
from vantage_sdk.core.http.models.search_options_facets_inner import (
    SearchOptionsFacetsInner,
)
from vantage_sdk.core.http.models.search_options_field_value_weighting import (
    SearchOptionsFieldValueWeighting,
)
from vantage_sdk.core.http.models.search_options_filter import (
    SearchOptionsFilter,
)
from vantage_sdk.core.http.models.search_options_pagination import (
    SearchOptionsPagination,
)
from vantage_sdk.core.http.models.search_options_sort import SearchOptionsSort
from vantage_sdk.core.http.models.total_counts_options_total_counts import (
    TotalCountsOptionsTotalCounts,
)


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class SemanticSearchQuery(BaseModel):
    """
    SemanticSearchQuery
    """  # noqa: E501

    collection: Optional[SearchOptionsCollection] = None
    request_id: Optional[StrictInt] = None
    filter: Optional[SearchOptionsFilter] = None
    field_value_weighting: Optional[SearchOptionsFieldValueWeighting] = None
    pagination: Optional[SearchOptionsPagination] = None
    sort: Optional[SearchOptionsSort] = None
    facets: Optional[List[SearchOptionsFacetsInner]] = None
    total_counts: Optional[TotalCountsOptionsTotalCounts] = None
    fields: Optional[List[StrictStr]] = None
    text: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "collection",
        "request_id",
        "filter",
        "field_value_weighting",
        "pagination",
        "sort",
        "facets",
        "total_counts",
        "fields",
        "text",
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
        """Create an instance of SemanticSearchQuery from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of field_value_weighting
        if self.field_value_weighting:
            _dict[
                'field_value_weighting'
            ] = self.field_value_weighting.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sort
        if self.sort:
            _dict['sort'] = self.sort.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in facets (list)
        _items = []
        if self.facets:
            for _item in self.facets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['facets'] = _items
        # override the default output from pydantic by calling `to_dict()` of total_counts
        if self.total_counts:
            _dict['total_counts'] = self.total_counts.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of SemanticSearchQuery from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "collection": SearchOptionsCollection.from_dict(
                    obj.get("collection")
                )
                if obj.get("collection") is not None
                else None,
                "request_id": obj.get("request_id"),
                "filter": SearchOptionsFilter.from_dict(obj.get("filter"))
                if obj.get("filter") is not None
                else None,
                "field_value_weighting": SearchOptionsFieldValueWeighting.from_dict(
                    obj.get("field_value_weighting")
                )
                if obj.get("field_value_weighting") is not None
                else None,
                "pagination": SearchOptionsPagination.from_dict(
                    obj.get("pagination")
                )
                if obj.get("pagination") is not None
                else None,
                "sort": SearchOptionsSort.from_dict(obj.get("sort"))
                if obj.get("sort") is not None
                else None,
                "facets": [
                    SearchOptionsFacetsInner.from_dict(_item)
                    for _item in obj.get("facets")
                ]
                if obj.get("facets") is not None
                else None,
                "total_counts": TotalCountsOptionsTotalCounts.from_dict(
                    obj.get("total_counts")
                )
                if obj.get("total_counts") is not None
                else None,
                "fields": obj.get("fields"),
                "text": obj.get("text"),
            }
        )
        return _obj
