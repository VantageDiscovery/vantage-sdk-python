from typing import Optional

from pydantic import BaseModel, StrictStr


class Account(BaseModel):
    id: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
