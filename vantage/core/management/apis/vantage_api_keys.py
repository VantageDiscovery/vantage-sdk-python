from vantage.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage.core.http.models import (
    VantageAPIKey,
    VantageAPIKeysResult,
)
from vantage.core.base import BaseAPI
from pydantic import StrictStr

__all__ = ["VantageAPIKeysAPI"]


class VantageAPIKeysAPI(BaseAPI):
    def get_vantage_api_keys(
        self, account_id: StrictStr
    ) -> VantageAPIKeysResult:
        # TODO: docstring
        return VantageAPIKeysApi.get_vantage_api_keys(account_id)

    def get_vantage_api_key(
        self, account_id: StrictStr, vantage_api_key_id: StrictStr
    ) -> VantageAPIKey:
        # TODO: docstring
        return VantageAPIKeysApi.get_vantage_api_key(
            account_id, vantage_api_key_id
        )
