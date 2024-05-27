"""
Models for the Search API.
"""

from typing import Any, List, Optional, Union

from pydantic import (
    BaseModel,
    StrictFloat,
    StrictInt,
    StrictStr,
    model_validator,
)

from vantage_sdk.core.http.models import (
    GlobalSearchPropertiesCollection,
    GlobalSearchPropertiesFieldValueWeighting,
    GlobalSearchPropertiesFilter,
    GlobalSearchPropertiesPagination,
    GlobalSearchPropertiesSort,
)


class SearchResultItem(BaseModel):
    """
    Represents an individual search result item.

    Attributes
    ----------
    id : Optional[StrictStr], optional
        The unique identifier of the document in the collection.
    score : Optional[Union[StrictFloat, StrictInt]], optional
        The similarity score associated with the document.
    """

    id: Optional[StrictStr] = None
    score: Optional[Union[StrictFloat, StrictInt]] = None


class SearchResult(BaseModel):
    """
    Represents the result received from all search methods.

    Attributes
    ----------
    request_id : Optional[StrictInt], optional
        The unique identifier for the search request.
    status : Optional[StrictInt], optional
        The status code of the search response.
    message : Optional[StrictStr], optional
        A message providing additional information about the search response.
    results : Optional[List[SearchResultItem]], optional
        A list of search result items returned by the search method.
    """

    request_id: Optional[StrictInt] = None
    status: Optional[StrictInt] = None
    message: Optional[StrictStr] = None
    results: Optional[List[SearchResultItem]] = None


class MoreLikeTheseItem(BaseModel):
    """
    Represents an item for "More Like These" queries.

    One of `query_text`, `query_document_id`, or `embedding` should be provided.

    Attributes
    ----------
    weight : StrictFloat
        The weight/importance assigned to this item in the query.
    query_text : StrictStr
        The text used for the query.
    query_document_id : Optional[StrictStr], optional
        The document ID used for the query.
    embedding : Optional[list[Union[StrictInt, StrictFloat]]], optional
        The embedding vector associated with the query.
    """

    weight: StrictFloat
    query_text: StrictStr
    query_document_id: Optional[StrictStr] = None
    embedding: Optional[list[StrictInt | StrictFloat]] = None
    these: Optional[list[dict[StrictStr, Any]]] = None

    @model_validator(mode="before")
    def check_mutually_exclusive_fields(cls, values):
        query_text = values.get('query_text')
        query_document_id = values.get('query_document_id')
        embedding = values.get('embedding')

        if (
            sum([bool(query_text), bool(query_document_id), bool(embedding)])
            > 1
        ):
            raise ValueError(
                'Only one of `query_text`, `query_document_id`, or `embedding` should be provided.'
            )

        if not any([query_text, query_document_id, embedding]):
            raise ValueError(
                'One of `query_text`, `query_document_id`, or `embedding` must be provided.'
            )

        return values


class GlobalSearchProperties(BaseModel):
    """
    Represents the global properties for all search methods.

    Attributes
    ----------
    collection : Optional[GlobalSearchPropertiesCollection], optional
        The collection properties.
    filter : Optional[GlobalSearchPropertiesFilter], optional
        The filter properties.
    pagination : Optional[GlobalSearchPropertiesPagination], optional
        The pagination properties.
    sort : Optional[GlobalSearchPropertiesSort], optional
        The sort properties.
    field_value_weighting : Optional[GlobalSearchPropertiesFieldValueWeighting], optional
        The field value weighting properties.
    """

    collection: Optional[GlobalSearchPropertiesCollection] = None
    filter: Optional[GlobalSearchPropertiesFilter] = None
    pagination: Optional[GlobalSearchPropertiesPagination] = None
    sort: Optional[GlobalSearchPropertiesSort] = None
    field_value_weighting: Optional[
        GlobalSearchPropertiesFieldValueWeighting
    ] = None
