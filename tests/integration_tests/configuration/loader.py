import os


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))
DISABLE_EXTERNAL_API_KEYS_TESTS = True


def _load_env() -> None:
    dotenv_path = os.path.join(PROJECT_DIR, "integration_tests", ".env")
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)


def _load_configuration() -> None:
    return {
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
        "collection": {
            "embedding_search_test_collection_id": os.getenv(
                "VANTAGE_EMBEDDING_SEARCH_TEST_COLLECTION_ID"
            ),
            "semantic_search_test_collection_id": os.getenv(
                "VANTAGE_SEMANTIC_SEARCH_TEST_COLLECTION_ID"
            ),
            "more_like_this_collection": os.getenv(
                "VANTAGE_MORE_LIKE_THIS_SEARCH_COLLECTION_ID"
            ),
        },
        "keys": {
            "vantage_api_key": os.getenv("VANTAGE_API_KEY"),
            "vantage_api_key_id": os.getenv("VANTAGE_API_KEY_ID"),
            "open_api_key": os.getenv("OPEN_API_KEY"),
            "open_api_key_id": os.getenv("OPEN_API_KEY_ID"),
            "external_api_key": os.getenv("EXTERNAL_API_KEY"),
            "external_api_key_id": os.getenv("EXTERNAL_API_KEY_ID"),
            "external_api_key_provider": os.getenv(
                "EXTERNAL_API_KEY_PROVIDER"
            ),
        },
        "auth": {
            "auth_method": os.getenv(
                "VANTAGE_AUTH_METHOD",
                "client_credentials",
            ),
            "jwt_token": os.getenv("VANTAGE_API_JWT_TOKEN", None),
        },
    }


_load_env()
CONFIGURATION = _load_configuration()
