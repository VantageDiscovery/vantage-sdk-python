# coding: utf-8

# flake8: noqa
"""
    Vantage API

    This is a the API to interact with Vantage Discovery, the amazing Semantic Search Platform in the world.  We enable developers to build magical discovery experiences into their products and websites.  Some useful links: - [TODO: Semantic Search Guide: What Is It And Why Does It Matter?](https://www.bloomreach.com/en/blog/2019/semantic-search-explained-in-5-minutes)

    The version of the OpenAPI document: v1.1.2
    Contact: devrel@vantagediscovery.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


# import models into model package
from vantage_sdk.core.http.models.account import Account
from vantage_sdk.core.http.models.account_modifiable import AccountModifiable
from vantage_sdk.core.http.models.account_read_only import AccountReadOnly
from vantage_sdk.core.http.models.collection import Collection
from vantage_sdk.core.http.models.collection_immutable import (
    CollectionImmutable,
)
from vantage_sdk.core.http.models.collection_modifiable import (
    CollectionModifiable,
)
from vantage_sdk.core.http.models.collection_read_only import (
    CollectionReadOnly,
)
from vantage_sdk.core.http.models.collection_upload_url import (
    CollectionUploadURL,
)
from vantage_sdk.core.http.models.create_collection_request import (
    CreateCollectionRequest,
)
from vantage_sdk.core.http.models.document_batch import DocumentBatch
from vantage_sdk.core.http.models.embedding_search_query import (
    EmbeddingSearchQuery,
)
from vantage_sdk.core.http.models.external_key import ExternalKey
from vantage_sdk.core.http.models.external_key_modifiable import (
    ExternalKeyModifiable,
)
from vantage_sdk.core.http.models.external_key_read_only import (
    ExternalKeyReadOnly,
)
from vantage_sdk.core.http.models.facet_range import FacetRange
from vantage_sdk.core.http.models.facet_result import FacetResult
from vantage_sdk.core.http.models.ml_these import MLThese
from vantage_sdk.core.http.models.ml_these_these_inner import MLTheseTheseInner
from vantage_sdk.core.http.models.more_like_these_query import (
    MoreLikeTheseQuery,
)
from vantage_sdk.core.http.models.more_like_this_query import MoreLikeThisQuery
from vantage_sdk.core.http.models.search_options import SearchOptions
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
from vantage_sdk.core.http.models.search_result import SearchResult
from vantage_sdk.core.http.models.search_result_results_inner import (
    SearchResultResultsInner,
)
from vantage_sdk.core.http.models.secondary_external_account import (
    SecondaryExternalAccount,
)
from vantage_sdk.core.http.models.semantic_search_query import (
    SemanticSearchQuery,
)
from vantage_sdk.core.http.models.shopping_assistant import ShoppingAssistant
from vantage_sdk.core.http.models.shopping_assistant_group_result import (
    ShoppingAssistantGroupResult,
)
from vantage_sdk.core.http.models.shopping_assistant_group_result_results_inner import (
    ShoppingAssistantGroupResultResultsInner,
)
from vantage_sdk.core.http.models.shopping_assistant_modifiable import (
    ShoppingAssistantModifiable,
)
from vantage_sdk.core.http.models.shopping_assistant_query import (
    ShoppingAssistantQuery,
)
from vantage_sdk.core.http.models.shopping_assistant_read_only import (
    ShoppingAssistantReadOnly,
)
from vantage_sdk.core.http.models.shopping_assistant_result import (
    ShoppingAssistantResult,
)
from vantage_sdk.core.http.models.total_count_response import (
    TotalCountResponse,
)
from vantage_sdk.core.http.models.total_counts_options import (
    TotalCountsOptions,
)
from vantage_sdk.core.http.models.total_counts_options_total_counts import (
    TotalCountsOptionsTotalCounts,
)
from vantage_sdk.core.http.models.vantage_api_key import VantageAPIKey
from vantage_sdk.core.http.models.vantage_vibe import VantageVibe
from vantage_sdk.core.http.models.vantage_vibe_image import VantageVibeImage
from vantage_sdk.core.http.models.vantage_vibe_modifiable import (
    VantageVibeModifiable,
)
from vantage_sdk.core.http.models.vantage_vibe_read_only import (
    VantageVibeReadOnly,
)
from vantage_sdk.core.http.models.vantage_vibe_search_query import (
    VantageVibeSearchQuery,
)
from vantage_sdk.core.http.models.weighted_field_values import (
    WeightedFieldValues,
)
