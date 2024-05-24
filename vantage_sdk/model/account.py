"""
Models for the Account API.
"""

from typing import Optional

from pydantic import BaseModel, StrictStr


class Account(BaseModel):
    """
    Represents user's account.

    Parameters
    ----------
    account_id : Optional[str]
        ID of the user's account.
    account_name : Optional[str]
        Name of the user's account.
    """

    account_id: Optional[StrictStr] = None
    account_name: Optional[StrictStr] = None
