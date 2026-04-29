from fastapi import APIRouter
from routes.llm.types import GetEmbedding, GetAnswer
#import requests
#from configs.configuration_parser import get_config_parser, CERT_PATH
#from json import JSONDecoder
from transformers import AutoModel
#import numpy as np
#import torch
#from transformers import pipeline
import time
import ollama
from typing import Dict, List


LLM_MODEL_NAME = "hdnh2006/salamandra-2b-instruct:Q5_1"

ollama.pull(LLM_MODEL_NAME)

# bitsandbytes

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
    responses={404: {"description": "Not found"}}
)


@router.post(path="/get_embeddings")
async def get_embeddings(data: GetEmbedding):
    model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
    embeddings = model.encode([data.text], task="text-matching")
    return embeddings[0].tolist()

PROMT = "Ты консультант на платформе онлайн-образования DpoCloud. Ответь на вопрос пользователя, основываясь исключительно на предоставленной" + \
        "информации о курсах на платформе. Отвечай только на том языке, на котором тебе задают вопрос (если вопрос задали " + \
        "на русском, то отвечай только на русском). Если вопрос не связан с платформой онлайн-образования, " + \
        "вежливо сообщи пользователю, что ты не специализируешься в этой области. Если из вопроса не понятно о каком конкретно " + \
        "курсе идет речь, то не отвечай на него, а выведи следующее сообщение: 'Пожалуйста, уточните, какой именно курс вас " + \
        "интересует'. Если в предоставленной информации о курсах нет ответа на вопрос, то предложи пользователю обратиться в " + \
        "техподдержку. Отвечай исключительно на поставленный вопрос, не выдавай излишнюю информацию. В своем ответе не генерируй " + \
        "новую информацию о платформе и курсах, которой нет в предоставленной информации о курсах. Не отвечай вопросом на вопрос. "

# Максимальное количество сообщений в истории
#MAX_HISTORY_LENGTH = 2

# Глобальный словарь для хранения истории диалога
#user_chat_histories: Dict[str, List[dict]] = {}

# @router.post(path="/get_answer")
# async def get_answer(data: GetAnswer, user_id: str):
#     # global user_chat_histories

#     # # Получаем историю диалога для пользователя
#     # if user_id not in user_chat_histories:
#     #     user_chat_histories[user_id] = []

#     # chat_history = user_chat_histories[user_id]

#     messages = [{"role": "system", "content": PROMT}]
#     # messages.extend(chat_history)
#     messages.append({"role": "assistant","content": "Информация о курсах на платформе DpoCloud: ".join(data.topics)})
#     messages.append({"role": "user", "content": data.question})

#     t1 = time.time()
#     response = ollama.chat(
#         model=LLM_MODEL_NAME,
#         messages=messages,
#         options={
#             "num_predict": 512,  # Ограничение по токенам
#             "temperature": 0.1
#         }
#     )
#     print(f"Elapsed: {time.time() - t1}")

#     # Получаем ответ модели
#     assistant_response = response["message"]["content"]

#     # #Добавляем текущий вопрос и ответ в историю диалога
#     # chat_history.append({"role": "user", "content": data.question})
#     # chat_history.append({"role": "assistant", "content": assistant_response})
#     # print(chat_history)
    
#     # # Ограничиваем длину истории
#     # if len(chat_history) > MAX_HISTORY_LENGTH:
#     #     chat_history = chat_history[-MAX_HISTORY_LENGTH:]

#     # # Сохраняем обновленную историю
#     # user_chat_histories[user_id] = chat_history

#     return {"answer": assistant_response}




@router.post(path="/get_answer")
async def get_answer(data: GetAnswer):
    messages = [{"role": "system", "content": PROMT}]
    messages.append({"role": "assistant","content": "Информация о курсах на платформе DpoCloud: ".join(data.topics)})
    messages.append({"role": "user", "content": data.question})
    response = ollama.chat(
        model=LLM_MODEL_NAME,
        messages=messages,
        # options={
        #     "num_predict": 512,
        #     "temperature": 0.001
        # }
    )
    return {"answer": response["message"]["content"]}
