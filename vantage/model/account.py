from typing import Optional

from pydantic import BaseModel, StrictStr


class Account(BaseModel):
    account_id: Optional[StrictStr] = None
    account_name: Optional[StrictStr] = None
