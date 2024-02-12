from typing import Any, Optional


class MoreLikeThese:
    def __init__(
        self,
        weight: int | float,
        query_text: str,
        query_document_id: Optional[str] = None,
        embedding: Optional[list[int | float]] = None,
        these: Optional[list[dict[str, Any]]] = None,
    ):
        self.weight = weight
        self.query_text = query_text
        self.query_document_id = query_document_id
        self.embedding = embedding
        self.these = these

    def to_dict(self):
        value = {}
        value["weight"] = self.weight
        value["query_text"] = self.query_text
        if self.query_document_id:
            value["query_document_id"] = self.query_document_id
        if self.embedding:
            value["embedding"] = self.embedding
        if self.these:
            value["these"] = self.these

        return value
