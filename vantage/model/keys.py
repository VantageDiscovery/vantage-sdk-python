from typing import Optional

from pydantic import BaseModel, StrictStr


class VantageAPIKey(BaseModel):
    vantage_api_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    vantage_api_key_created_date: Optional[StrictStr] = None
    vantage_api_key_value: Optional[StrictStr] = None


class ExternalAPIKey(BaseModel):
    external_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    external_key_created_date: Optional[StrictStr] = None
    url: Optional[StrictStr] = None
    llm_provider: Optional[StrictStr] = None
    llm_secret: Optional[StrictStr] = None
