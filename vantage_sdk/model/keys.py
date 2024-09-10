"""
Models for the Keys API.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, StrictStr


class VantageAPIKey(BaseModel):
    """
    Key for accessing Vantage API.

    Attributes
    ----------
    vantage_api_key_id: Optional[StrictStr]
        The unique identifier of the Vantage API key.
    account_id : Optional[str], optional
        The unique identifier of the account for which the Vantage API key is associated.
    vantage_api_key_obfuscated: Optional[StrictStr]
        Obfuscated value of the Vantage API key.
    status: Optional[StrictStr]
        Key status.
    """

    vantage_api_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    vantage_api_key_created_date: Optional[StrictStr] = None
    vantage_api_key_obfuscated: Optional[StrictStr] = None
    status: Optional[StrictStr] = None


class LLMProvider(Enum):
    """Supported LLM providers."""

    HuggingFace = "Hugging"
    OpenAI = "OpenAI"
    Anthropic = "Anthropic"


class ExternalKey(BaseModel):
    """
    Key for accessing one of the external APIs.

    Attributes
    ----------
    external_key_id: Optional[StrictStr]
        The unique identifier of the external API key.
    account_id: Optional[StrictStr]
        The unique identifier of the account for which the Vantage API key is associated.
    external_key_created_date: Optional[StrictStr]
        Date when the key was created in the user account.
    llm_provider: Optional[StrictStr]
        For which LLM provider this key is intended.
    llm_secret: Optional[StrictStr]
        External key secret value.
    state: Optional[StrictStr]
        External key state.
    """

    external_key_id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    external_key_created_date: Optional[StrictStr] = None
    llm_provider: Optional[StrictStr] = None
    llm_secret: Optional[StrictStr] = None
    state: Optional[StrictStr] = None


class SecondaryExternalAccount(BaseModel):
    """
    Secondary external account data.

    Attributes
    ----------
    external_account_id: Optional[StrictStr]
        Unique identifier of the external account.
    external_type: Optional[StrictStr]
        Type of the external account.
    """

    external_account_id: Optional[StrictStr] = None
    external_type: Optional[StrictStr] = None
