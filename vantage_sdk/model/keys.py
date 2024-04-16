from enum import Enum
from typing import Optional

from pydantic import BaseModel, StrictStr


class VantageAPIKey(BaseModel):
    vantage_api_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    vantage_api_key_created_date: Optional[StrictStr] = None
    vantage_api_key_obfuscated: Optional[StrictStr] = None
    status: Optional[StrictStr] = None


class LLMProvider(Enum):
    HuggingFace = "Hugging"
    OpenAI = "OpenAI"


class ExternalAPIKey(BaseModel):
    external_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    external_key_created_date: Optional[StrictStr] = None
    llm_provider: Optional[StrictStr] = None
    llm_secret: Optional[StrictStr] = None
    state: Optional[StrictStr] = None


class SecondaryExternalAccount(BaseModel):
    external_account_id: Optional[StrictStr] = None
    external_type: Optional[StrictStr] = None
