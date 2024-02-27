from typing import Optional

from pydantic import BaseModel, StrictStr


class VantageAPIKey(BaseModel):
    id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    created_date: Optional[StrictStr] = None
    value: Optional[StrictStr] = None


class ExternalAPIKey(BaseModel):
    id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    created_date: Optional[StrictStr] = None
    url: Optional[StrictStr] = None
    llm_provider: Optional[StrictStr] = None
    llm_secret: Optional[StrictStr] = None
