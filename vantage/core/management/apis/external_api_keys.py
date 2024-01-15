from vantage.core.http.api.external_api_keys_api import ExternalAPIKeysApi
from vantage.core.http.models import (
    ExternalAPIKey,
    ExternalAPIKeyModifiable,
    ExternalAPIKeysResult,
)
from vantage.core.base import BaseAPI
from pydantic import StrictStr

__all__ = ["ExternalAPIKeysAPI"]


class ExternalAPIKeysAPI(BaseAPI):
    def get_external_api_keys(
        self,
        account_id: StrictStr,
    ) -> ExternalAPIKeysResult:
        # TODO: docstring
        return ExternalAPIKeysApi.get_external_api_keys(account_id)

    def get_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
    ) -> ExternalAPIKey:
        # TODO: docstring
        return ExternalAPIKeysApi.get_external_api_key(
            account_id, external_key_id
        )

    def update_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
        external_api_key_modifiable: ExternalAPIKeyModifiable,
    ) -> ExternalAPIKey:
        # TODO: docstring
        return ExternalAPIKeysApi.update_external_api_key(
            account_id, external_key_id, external_api_key_modifiable
        )

    def delete_external_api_key(
        self,
        account_id: StrictStr,
        external_key_id: StrictStr,
    ) -> None:
        # TODO: docstring
        return ExternalAPIKeysApi.delete_external_api_key(
            account_id, external_key_id
        )
