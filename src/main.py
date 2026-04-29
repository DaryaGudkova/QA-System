from fastapi import FastAPI
from fastapi.responses import Response
from routes.elastic_search import routes as esr
from routes.llm import routes as llmr
from routes.main import routes as mr


app = FastAPI(version="v1")

app.include_router(esr.router)
app.include_router(llmr.router)
app.include_router(mr.router)