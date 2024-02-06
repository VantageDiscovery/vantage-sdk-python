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
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, StrictInt
from vantage.core.http.models.global_search_properties_collection import GlobalSearchPropertiesCollection
from vantage.core.http.models.global_search_properties_filter import GlobalSearchPropertiesFilter
from vantage.core.http.models.global_search_properties_pagination import GlobalSearchPropertiesPagination

class GlobalSearchProperties(BaseModel):
    """
    GlobalSearchProperties
    """
    collection: Optional[GlobalSearchPropertiesCollection] = None
    request_id: Optional[StrictInt] = None
    filter: Optional[GlobalSearchPropertiesFilter] = None
    pagination: Optional[GlobalSearchPropertiesPagination] = None
    __properties = ["collection", "request_id", "filter", "pagination"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> GlobalSearchProperties:
        """Create an instance of GlobalSearchProperties from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of collection
        if self.collection:
            _dict['collection'] = self.collection.to_dict()
        # override the default output from pydantic by calling `to_dict()` of filter
        if self.filter:
            _dict['filter'] = self.filter.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GlobalSearchProperties:
        """Create an instance of GlobalSearchProperties from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GlobalSearchProperties.parse_obj(obj)

        _obj = GlobalSearchProperties.parse_obj({
            "collection": GlobalSearchPropertiesCollection.from_dict(obj.get("collection")) if obj.get("collection") is not None else None,
            "request_id": obj.get("request_id"),
            "filter": GlobalSearchPropertiesFilter.from_dict(obj.get("filter")) if obj.get("filter") is not None else None,
            "pagination": GlobalSearchPropertiesPagination.from_dict(obj.get("pagination")) if obj.get("pagination") is not None else None
        })
        return _obj


