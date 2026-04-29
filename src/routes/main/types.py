from pydantic import BaseModel
from routes.elastic_search.types import *
from routes.llm.types import *


class CompleationsAddTopic(GetEmbedding):
    pass


class GetAnswer(GetEmbedding):
    pass