from pydantic import BaseModel


class CreateIndex(BaseModel):
    index_name: str

class DeleteIndex(BaseModel):
    index_name: str

class AddTopic(BaseModel):
    content: str
    embedding: list[float]

class DeleteTopic(BaseModel):
    topic_id: str

class EmbedSearchTopic(BaseModel):
    embedding: list[float]
    k: int
    num_candidates: int
