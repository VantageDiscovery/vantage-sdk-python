# coding: utf-8

"""
    Vantage API

    This is a the API to interact with Vantage Discovery, the amazing Semantic Search Platform in the world.  We enable developers to build magical discovery experiences into their products and websites.  Some useful links: - [TODO: Semantic Search Guide: What Is It And Why Does It Matter?](https://www.bloomreach.com/en/blog/2019/semantic-search-explained-in-5-minutes)

    The version of the OpenAPI document: v1.1.2
    Contact: devrel@vantagediscovery.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import io
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field, StrictFloat, StrictInt, StrictStr, validate_call


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from typing import Optional

from pydantic import Field, StrictStr
from typing_extensions import Annotated

from vantage_sdk.core.http.api_client import ApiClient
from vantage_sdk.core.http.api_response import ApiResponse
from vantage_sdk.core.http.models.documents_fields_query import (
    DocumentsFieldsQuery,
)
from vantage_sdk.core.http.models.documents_fields_query_response import (
    DocumentsFieldsQueryResponse,
)
from vantage_sdk.core.http.rest import RESTResponseType


class DocumentsApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    def documents_fields_query(
        self,
        account_id: Annotated[
            StrictStr, Field(description="The account to get information on")
        ],
        collection_id: Annotated[
            StrictStr,
            Field(description="Collection containing documents for the query"),
        ],
        documents_fields_query: Annotated[
            Optional[DocumentsFieldsQuery],
            Field(
                description="The JSON that describes how Vantage should query collection for documents"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> DocumentsFieldsQueryResponse:
        """Documents fields query

        Documents fields query

        :param account_id: The account to get information on (required)
        :type account_id: str
        :param collection_id: Collection containing documents for the query (required)
        :type collection_id: str
        :param documents_fields_query: The JSON that describes how Vantage should query collection for documents
        :type documents_fields_query: DocumentsFieldsQuery
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._documents_fields_query_serialize(
            account_id=account_id,
            collection_id=collection_id,
            documents_fields_query=documents_fields_query,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DocumentsFieldsQueryResponse",
            '206': "DocumentsFieldsQueryResponse",
            '404': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    def documents_fields_query_with_http_info(
        self,
        account_id: Annotated[
            StrictStr, Field(description="The account to get information on")
        ],
        collection_id: Annotated[
            StrictStr,
            Field(description="Collection containing documents for the query"),
        ],
        documents_fields_query: Annotated[
            Optional[DocumentsFieldsQuery],
            Field(
                description="The JSON that describes how Vantage should query collection for documents"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[DocumentsFieldsQueryResponse]:
        """Documents fields query

        Documents fields query

        :param account_id: The account to get information on (required)
        :type account_id: str
        :param collection_id: Collection containing documents for the query (required)
        :type collection_id: str
        :param documents_fields_query: The JSON that describes how Vantage should query collection for documents
        :type documents_fields_query: DocumentsFieldsQuery
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._documents_fields_query_serialize(
            account_id=account_id,
            collection_id=collection_id,
            documents_fields_query=documents_fields_query,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DocumentsFieldsQueryResponse",
            '206': "DocumentsFieldsQueryResponse",
            '404': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    def documents_fields_query_without_preload_content(
        self,
        account_id: Annotated[
            StrictStr, Field(description="The account to get information on")
        ],
        collection_id: Annotated[
            StrictStr,
            Field(description="Collection containing documents for the query"),
        ],
        documents_fields_query: Annotated[
            Optional[DocumentsFieldsQuery],
            Field(
                description="The JSON that describes how Vantage should query collection for documents"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Documents fields query

        Documents fields query

        :param account_id: The account to get information on (required)
        :type account_id: str
        :param collection_id: Collection containing documents for the query (required)
        :type collection_id: str
        :param documents_fields_query: The JSON that describes how Vantage should query collection for documents
        :type documents_fields_query: DocumentsFieldsQuery
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._documents_fields_query_serialize(
            account_id=account_id,
            collection_id=collection_id,
            documents_fields_query=documents_fields_query,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "DocumentsFieldsQueryResponse",
            '206': "DocumentsFieldsQueryResponse",
            '404': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _documents_fields_query_serialize(
        self,
        account_id,
        collection_id,
        documents_fields_query,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> Tuple:
        _host = None

        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, str] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if account_id is not None:
            _path_params['account_id'] = account_id
        if collection_id is not None:
            _path_params['collection_id'] = collection_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if documents_fields_query is not None:
            _body_params = documents_fields_query

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json']
        )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = self.api_client.select_header_content_type(
                ['application/json']
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = ['BearerAuth']

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1/document/{account_id}/{collection_id}',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )

    @validate_call
    def upload_documents(
        self,
        account_id: Annotated[StrictStr, Field(description="The account id")],
        collection_id: Annotated[
            StrictStr,
            Field(description="The collection to upload these documents into"),
        ],
        body: Annotated[
            StrictStr,
            Field(
                description="JSONL data, in vantage format, to upload to collection"
            ),
        ],
        customer_batch_identifier: Annotated[
            Optional[StrictStr],
            Field(
                description="If you have an identifier for this group of records in your system."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> None:
        """Upload Documents

        Upload documents to a collection for indexing

        :param account_id: The account id (required)
        :type account_id: str
        :param collection_id: The collection to upload these documents into (required)
        :type collection_id: str
        :param body: JSONL data, in vantage format, to upload to collection (required)
        :type body: str
        :param customer_batch_identifier: If you have an identifier for this group of records in your system.
        :type customer_batch_identifier: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._upload_documents_serialize(
            account_id=account_id,
            collection_id=collection_id,
            body=body,
            customer_batch_identifier=customer_batch_identifier,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': None,
            '405': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    def upload_documents_with_http_info(
        self,
        account_id: Annotated[StrictStr, Field(description="The account id")],
        collection_id: Annotated[
            StrictStr,
            Field(description="The collection to upload these documents into"),
        ],
        body: Annotated[
            StrictStr,
            Field(
                description="JSONL data, in vantage format, to upload to collection"
            ),
        ],
        customer_batch_identifier: Annotated[
            Optional[StrictStr],
            Field(
                description="If you have an identifier for this group of records in your system."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[None]:
        """Upload Documents

        Upload documents to a collection for indexing

        :param account_id: The account id (required)
        :type account_id: str
        :param collection_id: The collection to upload these documents into (required)
        :type collection_id: str
        :param body: JSONL data, in vantage format, to upload to collection (required)
        :type body: str
        :param customer_batch_identifier: If you have an identifier for this group of records in your system.
        :type customer_batch_identifier: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._upload_documents_serialize(
            account_id=account_id,
            collection_id=collection_id,
            body=body,
            customer_batch_identifier=customer_batch_identifier,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': None,
            '405': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    def upload_documents_without_preload_content(
        self,
        account_id: Annotated[StrictStr, Field(description="The account id")],
        collection_id: Annotated[
            StrictStr,
            Field(description="The collection to upload these documents into"),
        ],
        body: Annotated[
            StrictStr,
            Field(
                description="JSONL data, in vantage format, to upload to collection"
            ),
        ],
        customer_batch_identifier: Annotated[
            Optional[StrictStr],
            Field(
                description="If you have an identifier for this group of records in your system."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)],
            ],
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Upload Documents

        Upload documents to a collection for indexing

        :param account_id: The account id (required)
        :type account_id: str
        :param collection_id: The collection to upload these documents into (required)
        :type collection_id: str
        :param body: JSONL data, in vantage format, to upload to collection (required)
        :type body: str
        :param customer_batch_identifier: If you have an identifier for this group of records in your system.
        :type customer_batch_identifier: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """  # noqa: E501

        _param = self._upload_documents_serialize(
            account_id=account_id,
            collection_id=collection_id,
            body=body,
            customer_batch_identifier=customer_batch_identifier,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': None,
            '405': None,
        }
        response_data = self.api_client.call_api(
            *_param, _request_timeout=_request_timeout
        )
        return response_data.response

    def _upload_documents_serialize(
        self,
        account_id,
        collection_id,
        body,
        customer_batch_identifier,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> Tuple:
        _host = None

        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, str] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if account_id is not None:
            _path_params['account_id'] = account_id
        if collection_id is not None:
            _path_params['collection_id'] = collection_id
        # process the query parameters
        if customer_batch_identifier is not None:
            _query_params.append(
                ('customer_batch_identifier', customer_batch_identifier)
            )

        # process the header parameters
        # process the form parameters
        # process the body parameter
        if body is not None:
            _body_params = body

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = self.api_client.select_header_content_type(
                ['text/plain']
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = ['BearerAuth']

        return self.api_client.param_serialize(
            method='POST',
            resource_path='/v1/account/{account_id}/collection/{collection_id}/documents',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )
