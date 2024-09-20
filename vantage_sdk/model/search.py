"""
Models for the Search API.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    BaseModel,
    StrictFloat,
    StrictInt,
    StrictStr,
    model_validator,
)

from vantage_sdk.core.http.models import (
    SearchOptionsCollection,
    SearchOptionsFacetsInner,
    SearchOptionsFieldValueWeighting,
    SearchOptionsFilter,
    SearchOptionsPagination,
    SearchOptionsSort,
    WeightedFieldValues,
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
    sort_score : Optional[Union[StrictFloat, StrictInt]], optional
        The sort score associated with the document.
    variants : Optional[Union[StrictFloat, StrictInt]], optional
        The top variants of the document.
    variants_full_list : Optional[Union[StrictFloat, StrictInt]], optional
        All variants of the document.
    """

    id: Optional[StrictStr] = None
    score: Optional[Union[StrictFloat, StrictInt]] = None
    sort_score: Optional[Union[StrictFloat, StrictInt]] = None
    variants: Optional[List[StrictStr]] = None
    variants_full_list: Optional[List[StrictStr]] = None


class FacetResultItem(BaseModel):
    facet: Optional[StrictStr] = None
    type: Optional[StrictStr] = None
    values: Optional[Dict[str, Any]] = None


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
    facets: Optional[List[FacetResultItem]], optional
        A list of facet result items returned by the search method.
    """

    request_id: Optional[StrictInt] = None
    status: Optional[StrictInt] = None
    message: Optional[StrictStr] = None
    results: Optional[List[SearchResultItem]] = None
    facets: Optional[List[FacetResultItem]] = None


class ApproximateResultsCountResult(BaseModel):
    """
    Represents the result received from Approximate Result Search.

    Attributes
    ----------
    total_count: Optional[StrictInt], optional
        Total count of documents within the specified threshold.
    """

    total_count: Optional[StrictInt] = None


class MoreLikeTheseItem(BaseModel):
    """
    Represents an item for "More Like These" queries.

    One of `query_text`, `query_document_id`, or `embedding` should be provided.

    Attributes
    ----------
    weight : StrictFloat
        The weight/importance assigned to this item in the query.
    query_text : Optional[StrictStr], optional
        The text used for the query.
    query_document_id : Optional[StrictStr], optional
        The document ID used for the query.
    embedding : Optional[list[Union[StrictInt, StrictFloat]]], optional
        The embedding vector associated with the query.
    """

    weight: StrictFloat
    query_text: Optional[StrictStr] = None
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


class Filter(BaseModel):
    boolean_filter: Optional[str] = None
    variant_filter: Optional[str] = None


class Pagination(BaseModel):
    page: Optional[int] = None
    count: Optional[int] = None
    threshold: Optional[int] = None


class Sort(BaseModel):
    field: Optional[str] = None
    order: Optional[str] = None
    mode: Optional[str] = None


class WeightedFieldValueItem(BaseModel):
    field: Optional[str] = None
    value: Optional[str] = None
    weight: Optional[float] = None


class FieldValueWeighting(BaseModel):
    query_key_word_max_overall_weight: Optional[float] = None
    query_key_word_weighting_mode: Optional[str] = None
    weighted_field_values: Optional[List[WeightedFieldValueItem]] = None

    # Pydantic Config
    class Config:
        arbitrary_types_allowed = True

    def pydantic_weighted_field_values(
        self,
    ) -> Optional[List[WeightedFieldValues]]:
        if not self.weighted_field_values:
            return None

        return [
            WeightedFieldValues(
                field=item.field,
                value=item.value,
                weight=item.weight,
            )
            for item in self.weighted_field_values
        ]


class FacetType(Enum):
    COUNT = "count"


class Facet(BaseModel):
    name: str
    type: FacetType
    values: Optional[List[str]] = []


class VantageVibeImageAllFields(BaseModel):
    url: Optional[str] = None
    base64: Optional[str] = None


class VantageVibeImageUrl(VantageVibeImageAllFields):
    def __init__(self, url):
        super().__init__(url=url)


class VantageVibeImageBase64(VantageVibeImageAllFields):
    def __init__(self, base64):
        super().__init__(base64=base64)


class SearchOptions(BaseModel):
    """
    Represents the global properties for all search methods.

    Attributes
    ----------
    collection : Optional[SearchOptionsCollection], optional
        The collection properties.
    filter : Optional[SearchOptionsFilter], optional
        The filter properties.
    pagination : Optional[SearchOptionsPagination], optional
        The pagination properties.
    sort : Optional[SearchOptionsSort], optional
        The sort properties.
    field_value_weighting : Optional[SearchOptionsFieldValueWeighting], optional
        The field value weighting properties.
    facets: Optional[List[SearchOptionsFacetsInner]], optional
        An array of objects that define the facets you want to use in your query.
    """

    collection: Optional[SearchOptionsCollection] = None
    filter: Optional[SearchOptionsFilter] = None
    pagination: Optional[SearchOptionsPagination] = None
    sort: Optional[SearchOptionsSort] = None
    field_value_weighting: Optional[SearchOptionsFieldValueWeighting] = None
    facets: Optional[List[SearchOptionsFacetsInner]] = None


class TotalCountsOptions(BaseModel):
    """
    Represents threshold value for documents similarity score.

    Attributes
    ----------
    min_score_threshold: Optional[Union[StrictFloat, StrictInt]]
        Minimum score value in range 0.0 to 1.0. Both limits are inclusive.
    max_score_threshold: Optional[Union[StrictFloat, StrictInt]]
        Maximum score value in range 0.0 to 1.0. Both limits are inclusive.
    """

    min_score_threshold: Optional[Union[StrictFloat, StrictInt]] = None
    max_score_threshold: Optional[Union[StrictFloat, StrictInt]] = None
