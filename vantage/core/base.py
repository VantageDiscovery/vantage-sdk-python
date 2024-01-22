import datetime
import json
from typing import Optional
from urllib import request

from vantage.core.http import ApiClient


# TODO: This client is a quick temporary solution,
#       it needs to be revised for production usage.
class AuthorizationClient:
    def __init__(
        self,
        vantage_client_id: str,
        vantage_client_secret: str,
        # TODO: change vantage_audience_url
        #       and sso_endpoint_url to production values
        vantage_audience_url: str = (
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
    def jwt_token(self, force: bool = False) -> str:
        if force:
            self._get_new_token()
            if self._jwt_token is None:
                raise ValueError("Authentication failed.")
            else:
                return self._jwt_token["token"]

        if self._jwt_token is None or self._has_expired():
            self._get_new_token()

        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

        return self._jwt_token["token"]


class BaseAPI:
    """Base class for HTTP API calls."""

    def __init__(
        self,
        api_key: str,
        host: Optional[str] = None,
        pool_threads: Optional[int] = 1,
    ):
        self.api_key = api_key
        # TODO: add config and default values
        self.host = (
            host if host else "https://api.dev-a.dev.vantagediscovery.com/"
        )
        self.api_client = ApiClient(pool_threads=pool_threads)
        self.api_client.set_default_header(
            "authorization", f"Bearer {api_key}"
        )
