import os


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))
DISABLE_EXTERNAL_API_KEYS_TESTS = True
MOCK_DOTENV_FILE = os.path.join(PROJECT_DIR, "integration_tests", "mock-env")


def _load_env() -> None:
    dotenv_path = os.path.join(PROJECT_DIR, "integration_tests", ".env")
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)
    elif os.path.exists(MOCK_DOTENV_FILE):
        from dotenv import load_dotenv

        load_dotenv(MOCK_DOTENV_FILE)
    else:
        raise FileNotFoundError("Could not find valid environment file.")


def should_enable_external_api_key_tests(is_mock_api: bool) -> bool:
    enable_tests_env = (
        True
        if os.getenv("DISABLE_EXTERNAL_API_KEYS_TESTS", "true") == "true"
        else False
    )
    return enable_tests_env or is_mock_api


def _load_configuration() -> None:
    configuration = {
        "api": {
            "client_id": os.getenv("VANTAGE_CLIENT_ID"),
            "client_secret": os.getenv("VANTAGE_CLIENT_SECRET"),
            "auth_host": os.getenv("VANTAGE_AUTH_HOST"),
            "api_host": os.getenv("VANTAGE_API_HOST"),
            "is_mock": (
                True if os.getenv("USE_MOCK_API", "false") == "true" else False
            ),
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
            "non_existing_collection_id": os.getenv(
                "NON_EXISTING_COLLECTION_ID"
            ),
            "collection_to_update_id": os.getenv("COLLECTION_TO_UPDATE_ID"),
            "collection_to_delete_id": os.getenv("COLLECTION_TO_DELETE_ID"),
            "collection_id": os.getenv("GENERAL_COLLECTION_ID"),
            "collection_name": os.getenv("GENERAL_COLLECTION_NAME"),
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
            "llm_secret": os.getenv("LLM_SECRET", None),
        },
        "auth": {
            "auth_method": os.getenv(
                "VANTAGE_AUTH_METHOD",
                "client_credentials",
            ),
            "jwt_token": os.getenv("VANTAGE_API_JWT_TOKEN", None),
        },
        "other": {
            "is_mock_api": (
                True if os.getenv("USE_MOCK_API", "false") == "true" else False
            )
        },
    }
    configuration["other"][
        "enable_external_api_tests"
    ] = should_enable_external_api_key_tests(
        configuration["other"]["is_mock_api"]
    )
    return configuration


_load_env()
CONFIGURATION = _load_configuration()
