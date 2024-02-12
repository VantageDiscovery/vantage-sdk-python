from typing import Any, Optional

from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr


class MoreLikeThese(BaseModel):
    weight: StrictInt | StrictFloat
    query_text: StrictStr
    query_document_id: Optional[StrictStr] = None
    embedding: Optional[list[StrictInt | StrictFloat]] = None
    these: Optional[list[dict[StrictStr, Any]]] = None
