from typing import Any, List, Optional, Union

from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr
from vantage.core.http.models import (
    GlobalSearchPropertiesCollection,
    GlobalSearchPropertiesFilter,
    GlobalSearchPropertiesPagination,
)


class SearchResultItem(BaseModel):
    id: Optional[StrictStr] = None
    score: Optional[Union[StrictFloat, StrictInt]] = None


class SearchResult(BaseModel):
    request_id: Optional[StrictInt] = None
    status: Optional[StrictInt] = None
    message: Optional[StrictStr] = None
    results: Optional[List[SearchResultItem]] = None


class MoreLikeTheseItem(BaseModel):
    weight: StrictInt | StrictFloat
    query_text: StrictStr
    query_document_id: Optional[StrictStr] = None
    embedding: Optional[list[StrictInt | StrictFloat]] = None
    these: Optional[list[dict[StrictStr, Any]]] = None


class GlobalSearchProperties(BaseModel):
    collection: GlobalSearchPropertiesCollection
    filter: GlobalSearchPropertiesFilter
    pagination: GlobalSearchPropertiesPagination
