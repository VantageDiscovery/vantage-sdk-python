from typing import Any

from vantage_sdk.client import VantageClient


def create_client(
    auth_method: str,
    jwt_token: str,
    configuration: dict[str, Any],
) -> VantageClient:
    vantage_client = None

    if auth_method == "api_key":
        api_key = configuration["keys"]["vantage_api_key"]

        if api_key is None:
            raise ValueError("Vantage API key unspecified.")

        vantage_client = VantageClient.using_vantage_api_key(
            vantage_api_key=api_key,
            account_id=configuration["account"]["id"],
            api_host=configuration["api"]["api_host"],
        )
    elif auth_method == "jwt_token":
        if jwt_token is None:
            raise ValueError("JWT token unspecified.")

        vantage_client = VantageClient.using_jwt_token(
            vantage_api_jwt_token=jwt_token,
            account_id=configuration["account"]["id"],
            api_host=configuration["api"]["api_host"],
        )
    elif auth_method == "client_credentials":
        client_id = configuration["api"]["client_id"]
        client_secret = configuration["api"]["client_secret"]

        if client_id is None or client_secret is None:
            raise ValueError("Missing client credentials.")

        vantage_client = VantageClient.using_client_credentials(
            vantage_client_id=configuration["api"]["client_id"],
            vantage_client_secret=configuration["api"]["client_secret"],
            api_host=configuration["api"]["api_host"],
            auth_host=configuration["api"]["auth_host"],
            account_id=configuration["account"]["id"],
        )
    else:
        raise ValueError(
            f"Unknown auth method in $VANTAGE_AUTH_METHOD: {auth_method}"
        )

    return vantage_client
