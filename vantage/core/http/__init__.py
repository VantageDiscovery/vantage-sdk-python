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


__version__ = "1.0.0"

# import apis into sdk package
from vantage.core.http.api.account_management_api import AccountManagementApi
from vantage.core.http.api.collection_management_api import (
    CollectionManagementApi,
)
from vantage.core.http.api.external_api_keys_api import ExternalAPIKeysApi
from vantage.core.http.api.external_keys_api import ExternalKeysApi
from vantage.core.http.api.search_api import SearchApi
from vantage.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage.core.http.api_client import ApiClient

# import ApiClient
from vantage.core.http.api_response import ApiResponse
from vantage.core.http.configuration import Configuration
from vantage.core.http.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)

# import models into sdk package
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
from vantage.core.http.models.embedding_search_query import (
    EmbeddingSearchQuery,
)
from vantage.core.http.models.embedding_search_query_filter import (
    EmbeddingSearchQueryFilter,
)
from vantage.core.http.models.embedding_search_query_full import (
    EmbeddingSearchQueryFull,
)
from vantage.core.http.models.embedding_search_query_full_all_of_collection import (
    EmbeddingSearchQueryFullAllOfCollection,
)
from vantage.core.http.models.embedding_search_query_pagination import (
    EmbeddingSearchQueryPagination,
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
from vantage.core.http.models.search_result import SearchResult
from vantage.core.http.models.search_result_results_inner import (
    SearchResultResultsInner,
)
from vantage.core.http.models.semantic_search_query import SemanticSearchQuery
from vantage.core.http.models.semantic_search_query_filter import (
    SemanticSearchQueryFilter,
)
from vantage.core.http.models.semantic_search_query_full import (
    SemanticSearchQueryFull,
)
from vantage.core.http.models.semantic_search_query_full_all_of_collection import (
    SemanticSearchQueryFullAllOfCollection,
)
from vantage.core.http.models.semantic_search_query_pagination import (
    SemanticSearchQueryPagination,
)
from vantage.core.http.models.user import User
from vantage.core.http.models.user_modifiable import UserModifiable
from vantage.core.http.models.user_read_only import UserReadOnly
from vantage.core.http.models.user_registration_fields import (
    UserRegistrationFields,
)
from vantage.core.http.models.vantage_api_key import VantageAPIKey
from vantage.core.http.models.vantage_api_keys_result_inner import (
    VantageAPIKeysResultInner,
)
