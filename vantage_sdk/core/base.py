from __future__ import annotations

import datetime
from typing import Optional

import requests

from vantage_sdk.config import (
    AUTH_ENDPOINT,
    DEFAULT_API_HOST,
    DEFAULT_AUTH_HOST,
    DEFAULT_ENCODING,
)
from vantage_sdk.core.http import ApiClient
from vantage_sdk.core.http.exceptions import UnauthorizedException


class AuthorizationClient:
    _DAY_IN_SECONDS = 86400

    def __init__(
        self,
        vantage_audience_url: str = DEFAULT_API_HOST,
        sso_endpoint_url: str = f"{DEFAULT_AUTH_HOST}{AUTH_ENDPOINT}",
        vantage_api_key: Optional[str] = None,
        vantage_client_id: Optional[str] = None,
        vantage_client_secret: Optional[str] = None,
        vantage_jwt_token: Optional[str] = None,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        self._check_credentials(
            vantage_api_key=vantage_api_key,
            vantage_client_id=vantage_client_id,
            vantage_client_secret=vantage_client_secret,
            vantage_jwt_token=vantage_jwt_token,
        )

        self._vantage_api_key = vantage_api_key
        self._vantage_client_id = vantage_client_id
        self._vantage_client_secret = vantage_client_secret
        self._vantage_audience_url = vantage_audience_url
        self._sso_endpoint_url = sso_endpoint_url
        self._encoding = encoding

        if vantage_jwt_token:
            now = datetime.datetime.now().timestamp() * 1000
            self._jwt_token = {
                "token": vantage_jwt_token,
                "valid_until": now + AuthorizationClient._DAY_IN_SECONDS,
            }
        else:
            self._jwt_token = None

    def _check_credentials(
        self,
        vantage_api_key: Optional[str] = None,
        vantage_client_id: Optional[str] = None,
        vantage_client_secret: Optional[str] = None,
        vantage_jwt_token: Optional[str] = None,
    ):
        if (
            not vantage_api_key
            and not vantage_jwt_token
            and not (vantage_client_id and vantage_client_secret)
        ):
            raise ValueError(
                (
                    "Please provide Vantage API key or Vantage JWT token, or both Client ID and secret. ",
                    "None of these was found.",
                )
            )

    def _authenticate(self) -> dict:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            "client_id": self._vantage_client_id,
            "client_secret": self._vantage_client_secret,
            "grant_type": "client_credentials",
            "audience": self._vantage_audience_url,
        }

        return requests.post(
            self._sso_endpoint_url, data=body, headers=headers
        ).json()

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
        if self._vantage_api_key or self._jwt_token:
            return

        authentication = self._authenticate()
        now = datetime.datetime.now().timestamp() * 1000
        self._jwt_token = {
            "token": authentication['access_token'],
            "valid_until": now + authentication["expires_in"],
        }

    @property
    def jwt_token(self) -> str:
        if self._jwt_token:
            return self._jwt_token["token"]

        if self._jwt_token is None or self._has_expired():
            self._get_new_token()

        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

        return self._jwt_token["token"]

    def authenticate(self):
        if self._vantage_api_key or self._jwt_token:
            return

        self._get_new_token()
        if self._jwt_token is None:
            raise ValueError("Authentication failed.")

    @classmethod
    def automatic_token_management(
        cls,
        vantage_api_key: str,
        vantage_client_id: str,
        vantage_client_secret: str,
        vantage_audience_url: str,
        sso_endpoint_url: str,
    ) -> AuthorizationClient:
        return cls(
            vantage_api_key=vantage_api_key,
            vantage_client_id=vantage_client_id,
            vantage_client_secret=vantage_client_secret,
            vantage_jwt_token=None,
            vantage_audience_url=vantage_audience_url,
            sso_endpoint_url=sso_endpoint_url,
        )

    @classmethod
    def using_provided_vantage_api_key(cls, vantage_api_key: str):
        return cls(vantage_api_key=vantage_api_key)

    @classmethod
    def using_provided_token(cls, vantage_jwt_token: str):
        return cls(vantage_jwt_token=vantage_jwt_token)


class AuthorizedApiClient(ApiClient):
    def __init__(
        self,
        authorization_client: AuthorizationClient,
        configuration=None,
        header_name=None,
        header_value=None,
        cookie=None,
    ) -> None:
        super().__init__(
            configuration=configuration,
            header_name=header_name,
            header_value=header_value,
            cookie=cookie,
        )
        self.authorization_client = authorization_client

    def call_api(
        self,
        method,
        url,
        header_params=None,
        body=None,
        post_params=None,
        _request_timeout=None,
    ):
        args = (
            method,
            url,
            header_params,
            body,
            post_params,
            _request_timeout,
        )
        if "authorization" in header_params:
            return super().call_api(*args)

        try:
            auth_string = (
                self.authorization_client._vantage_api_key
                if self.authorization_client._vantage_api_key
                else self.authorization_client.jwt_token
            )
            header_params["authorization"] = f"Bearer {auth_string}"
            return super().call_api(*args)
        except UnauthorizedException:
            self.authorization_client.authenticate()
            header_params[
                "authorization"
            ] = f"Bearer {self.authorization_client.jwt_token}"
            return super().call_api(*args)
