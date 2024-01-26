from __future__ import annotations

import datetime
import json
from urllib import request

from vantage.core.http import ApiClient
from vantage.core.http.exceptions import UnauthorizedException


# TODO: This client is a quick temporary solution,
#       it needs to be revised for production usage.
class AuthorizationClient:
    _DAY_IN_SECONDS = 86400

    def __init__(
        self,
        vantage_audience_url: str,
        sso_endpoint_url: str,
        vantage_client_id: str = None,
        vantage_client_secret: str = None,
        vantage_jwt_token: str = None,
        encoding: str = "utf-8",
    ) -> None:
        if vantage_jwt_token:
            if (
                vantage_client_id is not None
                or vantage_client_secret is not None
            ):
                raise ValueError(
                    "Use either client id and secret, or JWT token, not both."
                )

        if vantage_jwt_token:
            now = datetime.datetime.now().timestamp() * 1000
            self._jwt_token = {
                "token": vantage_jwt_token,
                "valid_until": now + AuthorizationClient._DAY_IN_SECONDS,
            }
            self._user_provided_token = True
            self._vantage_client_id = None
            self._vantage_client_secret = None
        else:
            self._user_provided_token = False
            self._vantage_client_id = vantage_client_id
            self._vantage_client_secret = vantage_client_secret
            self._jwt_token = None

        self._vantage_audience_url = vantage_audience_url
        self._sso_endpoint_url = sso_endpoint_url
        self._encoding = encoding

    def _authenticate(self) -> dict:
        if self._user_provided_token:
            return

        headers = {"content-type": "application/json"}
        body = {
            "client_id": self._vantage_client_id,
            "client_secret": self._vantage_client_secret,
            "audience": self._vantage_audience_url,
            "grant_type": "client_credentials",
        }
        data = str.encode(json.dumps(body), encoding=self._encoding)
        get_token_request = request.Request(
            url=self._sso_endpoint_url,
            data=data,
            headers=headers,
            method="POST",
        )

        with request.urlopen(get_token_request) as response:
            response_body = response.read().decode(self._encoding)
            return json.loads(response_body)

    def _has_expired(self) -> bool:
        if self._jwt_token is None:
            self._get_new_token()

        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

        valid_until = self._jwt_token["valid_until"]
        now = datetime.datetime.now().timestamp() * 1000

        # Subtracting 5s not to wait for the last moment to obtain new token.
        return (valid_until - 5000) - now >= 0

    def _get_new_token(self):
        if self._user_provided_token:
            return
        authentication = self._authenticate()
        now = datetime.datetime.now().timestamp() * 1000
        self._jwt_token = {
            "token": authentication['access_token'],
            "valid_until": now + authentication["expires_in"],
        }

    @property
    def jwt_token(self) -> str:
        if self._user_provided_token:
            return self._jwt_token["token"]

        if self._jwt_token is None or self._has_expired():
            self._get_new_token()

        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

        return self._jwt_token["token"]

    def authenticate(self):
        if self._user_provided_token:
            return

        self._get_new_token()
        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

    @classmethod
    def automatic_token_management(
        cls,
        vantage_client_id: str,
        vantage_client_secret: str,
        vantage_audience_url: str,
        sso_endpoint_url: str,
    ) -> AuthorizationClient:
        return cls(
            vantage_client_id=vantage_client_id,
            vantage_client_secret=vantage_client_secret,
            vantage_jwt_token=None,
            vantage_audience_url=vantage_audience_url,
            sso_endpoint_url=sso_endpoint_url,
        )

    @classmethod
    def using_provided_token(
        cls,
        vantage_jwt_token: str,
        vantage_audience_url: str,
        sso_endpoint_url: str,
    ):
        return cls(
            vantage_client_id=None,
            vantage_client_secret=None,
            vantage_jwt_token=vantage_jwt_token,
            vantage_audience_url=vantage_audience_url,
            sso_endpoint_url=sso_endpoint_url,
        )


class AuthorizedApiClient(ApiClient):
    def __init__(
        self,
        authorization_client: AuthorizationClient,
        configuration=None,
        header_name=None,
        header_value=None,
        cookie=None,
        pool_threads=1,
    ) -> None:
        super().__init__(
            configuration=configuration,
            header_name=header_name,
            header_value=header_value,
            cookie=cookie,
            pool_threads=pool_threads,
        )
        self.authorization_client = authorization_client

    def call_api(
        self,
        resource_path,
        method,
        path_params=None,
        query_params=None,
        header_params=None,
        body=None,
        post_params=None,
        files=None,
        response_types_map=None,
        auth_settings=None,
        async_req=None,
        _return_http_data_only=None,
        collection_formats=None,
        _preload_content=True,
        _request_timeout=None,
        _host=None,
        _request_auth=None,
    ):
        args = (
            resource_path,
            method,
            path_params,
            query_params,
            header_params,
            body,
            post_params,
            files,
            response_types_map,
            auth_settings,
            async_req,
            _return_http_data_only,
            collection_formats,
            _preload_content,
            _request_timeout,
            _host,
            _request_auth,
        )
        if "authorization" in header_params:
            return super().call_api(*args)

        try:
            header_params[
                "authorization"
            ] = f"Bearer {self.authorization_client.jwt_token}"
            return super().call_api(*args)
        except UnauthorizedException:
            self.authorization_client.authenticate()
            header_params[
                "authorization"
            ] = f"Bearer {self.authorization_client.jwt_token}"
            return super().call_api(*args)
