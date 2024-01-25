# SDK Tests

## Preconditions

Running the tests against live API requires few environment variables to be set:

```
VANTAGE_CLIENT_ID=auth client ID
VANTAGE_CLIENT_SECRET=auth client secret
VANTAGE_AUTH_HOST=vantage auth host
VANTAGE_API_HOST=vantage API host
TEST_ACCOUNT_ID=test account ID
TEST_ACCOUNT_NAME=test account name
```

When running integration tests against live API, keep in mind that real data will be created and deleted using the provided account ID.

Preferred way to set the environment variables for tests is to set them in `tests/integration_tests/.env` file, and tests will automatically pick them up from there. There is an example file provided in `tests/integration_tests/.env-example`.

## Running tests

Setup your development environment and install all of the dependencies, as specified in `docs/DeveloperREADME.md`.

Running tests is done by issuing `make test`. or `make unittest` (if you want to skip running formatter and linter) at the project root. Alternatively, if you don't have `make` installed, just run `pytest` at the project root.
