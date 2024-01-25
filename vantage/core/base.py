import datetime
import json
from typing import Optional
from urllib import request

from vantage.core.http import ApiClient
from vantage.core.http.exceptions import UnauthorizedException


# TODO: This client is a quick temporary solution,
#       it needs to be revised for production usage.
class AuthorizationClient:
    def __init__(
        self,
        vantage_client_id: str,
        vantage_client_secret: str,
        # TODO: change vantage_audience_url
        #       and sso_endpoint_url to production values
        vantage_audience_url: Optional[str] = (
            "https://api.dev-a.dev.vantagediscovery.com"
        ),
        sso_endpoint_url: str = (
            "https://vantage-dev.us.auth0.com/oauth/token"
        ),
        encoding: str = "utf-8",
    ) -> None:
        self._vantage_client_id = vantage_client_id
        self._vantage_client_secret = vantage_client_secret
        self._vantage_audience_url = vantage_audience_url
        self._sso_endpoint_url = sso_endpoint_url
        self._encoding = encoding
        self._jwt_token = None

    def _authenticate(self) -> dict:
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
        authentication = self._authenticate()
        now = datetime.datetime.now().timestamp() * 1000
        self._jwt_token = {
            "token": authentication['access_token'],
            "valid_until": now + authentication["expires_in"],
        }

    @property
    def jwt_token(self) -> str:
        if self._jwt_token is None or self._has_expired():
            self._get_new_token()

        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

        return self._jwt_token["token"]

    def authenticate(self):
        self._get_new_token()
        if self._jwt_token is None:
            raise ValueError("Authentication failed.")


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
