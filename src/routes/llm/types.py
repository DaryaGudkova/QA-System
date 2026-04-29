from pydantic import BaseModel


class GetEmbedding(BaseModel):
    text: str

class GetAnswer(BaseModel):
    question: str
    topics: list[str]