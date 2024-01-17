from pydantic import StrictStr  # type: ignore

from vantage.core.base import BaseAPI
from vantage.core.http.api.external_api_keys_api import ExternalAPIKeysApi
from vantage.core.http.models import (
    ExternalAPIKey,
    ExternalAPIKeyModifiable,
    ExternalAPIKeysResult,
)


__all__ = ["ExternalAPIKeysAPI"]


class ExternalAPIKeysAPI(BaseAPI):
    def __init__(
        self, api_key: str, host: str | None, pool_threads: int | None = 1
    ):
        super().__init__(api_key, host, pool_threads)
        self.api = ExternalAPIKeysApi(api_client=self.api_client)

    def get_external_api_keys(
        self,
        account_id: StrictStr,
    ) -> ExternalAPIKeysResult:
        # TODO: docstring
        return self.api.get_external_api_keys(account_id)

    def get_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
    ) -> ExternalAPIKey:
        # TODO: docstring
        return self.api.get_external_api_key(account_id, external_key_id)

    def update_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
        external_api_key_modifiable: ExternalAPIKeyModifiable,
    ) -> ExternalAPIKey:
        # TODO: docstring
        return self.api.update_external_api_key(
            account_id, external_key_id, external_api_key_modifiable
        )

    def delete_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
    ) -> None:
        # TODO: docstring
        return self.api.delete_external_api_key(account_id, external_key_id)
