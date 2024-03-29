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
from vantage.core.http.models.account import Account
from vantage.core.http.models.account_modifiable import AccountModifiable
from vantage.core.http.models.account_read_only import AccountReadOnly
from vantage.core.http.models.collection import Collection
from vantage.core.http.models.collection_immutable import CollectionImmutable
from vantage.core.http.models.collection_modifiable import CollectionModifiable
from vantage.core.http.models.collection_read_only import CollectionReadOnly
from vantage.core.http.models.collection_upload_url import CollectionUploadURL
from vantage.core.http.models.collections_result_inner import (
    CollectionsResultInner,
)
from vantage.core.http.models.create_collection_request import (
    CreateCollectionRequest,
)
from vantage.core.http.models.document_batch import DocumentBatch
from vantage.core.http.models.embedding_search_query import (
    EmbeddingSearchQuery,
)
from vantage.core.http.models.external_api_key import ExternalAPIKey
from vantage.core.http.models.external_api_key_modifiable import (
    ExternalAPIKeyModifiable,
)
from vantage.core.http.models.external_api_key_read_only import (
    ExternalAPIKeyReadOnly,
)
from vantage.core.http.models.external_api_keys_result_inner import (
    ExternalAPIKeysResultInner,
)
from vantage.core.http.models.global_search_properties import (
    GlobalSearchProperties,
)
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
from vantage.core.http.models.ml_these import MLThese
from vantage.core.http.models.ml_these_these_inner import MLTheseTheseInner
from vantage.core.http.models.more_like_these_query import MoreLikeTheseQuery
from vantage.core.http.models.more_like_this_query import MoreLikeThisQuery
from vantage.core.http.models.search_result import SearchResult
from vantage.core.http.models.search_result_results_inner import (
    SearchResultResultsInner,
)
from vantage.core.http.models.semantic_search_query import SemanticSearchQuery
from vantage.core.http.models.vantage_api_key import VantageAPIKey
from vantage.core.http.models.vantage_api_keys_result_inner import (
    VantageAPIKeysResultInner,
)
