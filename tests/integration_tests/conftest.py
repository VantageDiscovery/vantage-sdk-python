import os
import random
import string
from typing import Callable

import pytest

from vantage.vantage import Vantage


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))


def _load_env() -> None:
    dotenv_path = os.path.join(
        PROJECT_DIR, "tests", "integration_tests", ".env"
    )
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)


_load_env()

_configuration = {
    "api": {
        "client_id": os.getenv("VANTAGE_CLIENT_ID"),
        "client_secret": os.getenv("VANTAGE_CLIENT_SECRET"),
        "auth_host": os.getenv("VANTAGE_AUTH_HOST"),
        "api_host": os.getenv("VANTAGE_API_HOST"),
    },
    "account": {
        "id": os.getenv("TEST_ACCOUNT_ID"),
        "name": os.getenv("TEST_ACCOUNT_NAME"),
    },
    "collection": {},
}

jwt_token = os.getenv("VANTAGE_API_JWT_TOKEN")

if jwt_token:
    _client = Vantage.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        account_id=_configuration["account"]["id"],
        api_host=_configuration["api"]["api_host"],
    )
else:
    _client = Vantage.using_client_credentials(
        vantage_client_id=_configuration["api"]["client_id"],
        vantage_client_secret=_configuration["api"]["client_secret"],
        api_host=_configuration["api"]["api_host"],
        auth_host=_configuration["api"]["auth_host"],
        account_id=_configuration["account"]["id"],
    )


def _random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope="module")
def api_params() -> dict:
    return _configuration["api"]


@pytest.fixture(scope="module")
def account_params() -> dict:
    return _configuration["account"]


@pytest.fixture(scope="module")
def collection_params() -> dict:
    return _configuration["collection"]


@pytest.fixture(scope="module")
def client() -> Vantage:
    return _client


@pytest.fixture(scope="module")
def random_string_generator() -> Callable:
    return _random_string


@pytest.fixture(scope="module")
def test_parquet_file_path() -> str:
    return "tests/data/hello_world.parquet"
