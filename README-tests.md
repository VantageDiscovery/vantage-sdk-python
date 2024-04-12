# SDK Tests

**NOTE**: Currently, tests for external API keys are disabled, since API introduced checking if OpenAI/HuggingFace keys are valid, and since we're running tests against live API, we cannot use mock keys. This will be addressed in the future.

## Preconditions

Running the tests against live API requires few environment variables to be set.
When running integration tests against live API, keep in mind that real data will be created and deleted using the provided account ID.

Preferred way to set the environment variables for tests is to set them in `tests/integration_tests/.env` file, and tests will automatically pick them up from there. There is an example file provided in `tests/integration_tests/.env-example`.

### Mandatory environment variables

There are 3 methods of authentication to the API: client credentials, api key, and jwt token. It is mandatory to have one of these set.
By default, the tests expect client credentials, but that can be overriden using `VANTAGE_AUTH_METHOD` variable:

```
VANTAGE_AUTH_METHOD=< api_key | client_credentials | jwt_token >
```

If using client credentials, these variables are mandatory:

```
VANTAGE_CLIENT_ID=xyz
VANTAGE_CLIENT_SECRET=xyz
```

If using API key:

```
VANTAGE_API_KEY=xyz
```

If using JWT token:

```
VANTAGE_API_JWT_TOKEN=xyz
```

Except for the authorization variables these are also mandatory to be set:

```
VANTAGE_AUTH_HOST=vantage auth host
VANTAGE_API_HOST=vantage API host
TEST_ACCOUNT_ID=test account ID
TEST_ACCOUNT_NAME=test account name
```

### Optional environment variables

Search tests need to have a set-up collection to run. If these variables are not set, they will be skipped.
```
VANTAGE_EMBEDDING_SEARCH_TEST_COLLECTION_ID=test-collection
VANTAGE_MORE_LIKE_THIS_SEARCH_COLLECTION_ID=test-collection
VANTAGE_SEMANTIC_SEARCH_TEST_COLLECTION_ID=test-collection
```

Tests for external APIs need following to be set, else they will be skipped.
```
EXTERNAL_API_KEY_ID=xyz
EXTERNAL_API_KEY=xyz
EXTERNAL_API_KEY_PROVIDER=OpenAI
```

If this variable is set to true, test deleting a real key will be executed.
```
ENABLE_DELETE_KEY_TEST=false
```

## Running tests

Setup your development environment and install all of the dependencies, as specified in `docs/DeveloperREADME.md`.

Running tests is done by issuing `make test`. or `make unittest` (if you want to skip running formatter and linter) at the project root. Alternatively, if you don't have `make` installed, just run `pytest` at the project root.
