from fastapi import APIRouter
from routes.elastic_search.types import CreateIndex, DeleteIndex, AddTopic, DeleteTopic, EmbedSearchTopic
import requests
from configs.configuration_parser import get_config_parser, CERT_PATH
from json import JSONDecoder


router = APIRouter(
    prefix="/elastic_search",
    tags=["elastic_search"],
    responses={404: {"description": "Not found"}}
)


ELASTIC_MAPPING = {
    "properties": {
        "content": {"type": "text"},
        "embedding": {"type": "dense_vector"}
    }
}


@router.post(path="/create_index")
async def create_index(data: CreateIndex):

    configparser = get_config_parser()

    response = requests.put(
        url=f"https://localhost:9200/{data.index_name}",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]),
        json={"mappings": ELASTIC_MAPPING})
    
    return response.json()

@router.delete(path="/{index}/delete_index")
async def delete_index(index: str):
    
    configparser = get_config_parser()
    
    response = requests.delete(
        url=f"https://localhost:9200/{index}",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]))
    
    return response.json()

@router.post(path="/{index}/add_topic")
async def add_topic(index: str, data: AddTopic):

    configparser = get_config_parser()

    response = requests.post(
        url=f"https://localhost:9200/{index}/_doc",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]),
        json=dict(data))
    return response.json()

@router.get(path="/{index}/get_all_topics")
async def get_all_topics(index: str):
    configparser = get_config_parser()

    response = requests.get(
        url=f"https://localhost:9200/{index}/_search",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]))
    
    return response.json()

@router.delete(path="/{index}/delete_topics/{topic_id}")
async def delete_topic(index: str, topic_id: str):
    configparser = get_config_parser()

    response = requests.delete(
        url=f"https://localhost:9200/{index}/_doc/{topic_id}",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]))
    
    return response.json()


@router.post(path="/{index}/search")
async def search_embed_topics(index: str, data: EmbedSearchTopic):
    configparser = get_config_parser()

    search_request = {
        "knn": {
            "field": "embedding",
            "query_vector": data.embedding,
            "k": data.k,
            "num_candidates": data.num_candidates
        }
    }

    response = requests.post(
        url=f"https://localhost:9200/{index}/_search",
        verify=CERT_PATH,
        headers={"Content-Type": "application/json"},
        auth=("elastic", configparser["elastic_search"]["ELASTIC_PASSWORD"]),
        json=search_request)
    
    return response.json()
