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
from vantage_sdk.core.http.api.account_management_api import (
    AccountManagementApi,
)
from vantage_sdk.core.http.api.collection_management_api import (
    CollectionManagementApi,
)
from vantage_sdk.core.http.api.documents_api import DocumentsApi
from vantage_sdk.core.http.api.external_keys_api import ExternalKeysApi
from vantage_sdk.core.http.api.search_api import SearchApi
from vantage_sdk.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage_sdk.core.http.api_client import ApiClient

# import ApiClient
from vantage_sdk.core.http.api_response import ApiResponse
from vantage_sdk.core.http.configuration import Configuration
from vantage_sdk.core.http.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)

# import models into sdk package
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
from vantage_sdk.core.http.models.global_search_properties import (
    GlobalSearchProperties,
)
from vantage_sdk.core.http.models.global_search_properties_collection import (
    GlobalSearchPropertiesCollection,
)
from vantage_sdk.core.http.models.global_search_properties_field_value_weighting import (
    GlobalSearchPropertiesFieldValueWeighting,
)
from vantage_sdk.core.http.models.global_search_properties_filter import (
    GlobalSearchPropertiesFilter,
)
from vantage_sdk.core.http.models.global_search_properties_pagination import (
    GlobalSearchPropertiesPagination,
)
from vantage_sdk.core.http.models.global_search_properties_sort import (
    GlobalSearchPropertiesSort,
)
from vantage_sdk.core.http.models.ml_these import MLThese
from vantage_sdk.core.http.models.ml_these_these_inner import MLTheseTheseInner
from vantage_sdk.core.http.models.more_like_these_query import (
    MoreLikeTheseQuery,
)
from vantage_sdk.core.http.models.more_like_this_query import MoreLikeThisQuery
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
from vantage_sdk.core.http.models.vantage_api_key import VantageAPIKey
from vantage_sdk.core.http.models.weighted_field_values import (
    WeightedFieldValues,
)
