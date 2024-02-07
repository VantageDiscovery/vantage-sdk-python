from typing import Any


class MoreLikeThese:
    def __init__(
        self,
        weight: int | float,
        query_text: str,
        query_document_id: str,
        embedding: list[int | float],
        these: list[dict[str:Any]],
    ):
        self.weight = weight
        self.query_text = query_text
        self.query_document_id = query_document_id
        self.embedding = embedding
        self.these = these

    def to_dict(self):
        return {
            "weight": self.weight,
            "query_text": self.query_text,
            "query_document_id": self.query_document_id,
            "embedding": self.embedding,
            "these": self.these,
        }
