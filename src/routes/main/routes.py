import routes.elastic_search.routes as es
import routes.llm.routes as llm
from routes.main.types import *
from fastapi import APIRouter, HTTPException
import os
import csv
from datetime import datetime

router = APIRouter(
    prefix="/main",
    tags=["main"],
    responses={404: {"description": "Not found"}}
)

#Функция для сохранения истории чата
def save_chat_history(question: str, answer: str, history_file: str = "chat_history.csv"):
    file_exists = os.path.exists(history_file)  
    with open(history_file, "a", encoding="utf-8", newline='') as h_file: 
        writer = csv.writer(h_file, delimiter=';')
        if not file_exists:
            writer.writerow(["Timestamp", "Question", "Answer"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        writer.writerow([timestamp, question, answer])

#ОСНОВНАЯ функция чат-бота
#отвечает на вопрос data, беря топики (чанки) из индекса index
@router.post("/get_answer")
async def get_answer(index: str, data: GetAnswer): #user_id: str,
    embedding = await llm.get_embeddings(data=data)
    topics = await es.search_embed_topics(index=index, data=es.EmbedSearchTopic(embedding=embedding, k=4, num_candidates=100))
    topics_prep = [a["_source"]["content"] for a in topics["hits"]["hits"]]
    answer = await llm.get_answer(llm.GetAnswer(question=data.text, topics=topics_prep)) #, user_id: str
    save_chat_history(question=data.text, answer=answer["answer"])
    return answer

#добавляет один топик data в индекс index
@router.post("/add_topic")
async def add_topic(index: str, data: CompleationsAddTopic):
    embedding = await llm.get_embeddings(data=data)
    result = await es.add_topic(index=index, data=es.AddTopic(content=data.text, embedding=embedding))
    return result

async def load_topics_from_file(index: str, file_path: str = "topics.txt"):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File 'topics.txt' not found")
    
    with open(file_path, "r", encoding="utf-8") as file:
        topics = file.readlines()
    
    for topic in topics:
        topic = topic.strip()
        if topic:
            embedding = await llm.get_embeddings(data=CompleationsAddTopic(text=topic))
            result = await es.add_topic(index=index, data=es.AddTopic(content=topic, embedding=embedding))
            print(f"Added topic: {topic}, result: {result}")

#загружает топики в индекс index из файла file_path
@router.post("/load_topics")
async def load_topics(index: str, file_path: str):
    await load_topics_from_file(index, file_path)
    return {"message": "Topics loaded successfully"}

#генерирует файл answers.csv с ответами на все вопросы из файла questions.txt
#используется для оценки качества
@router.post("/generate_answers")
async def generate_answers(index: str, questions_file: str = "questions.txt", answers_file: str = "answers.csv"): #user_id: str, 
    if not os.path.exists(questions_file):
        raise HTTPException(status_code=404, detail=f"File '{questions_file}' not found")
    
    with open(questions_file, "r", encoding="utf-8") as q_file, open(answers_file, "w", encoding="utf-8", newline='') as a_file:
        questions = q_file.readlines()
        writer = csv.writer(a_file, delimiter=';')
        
        for question in questions:
            question = question.strip()
            if question:
                answer = await get_answer(index=index, data=GetAnswer(text=question)) #user_id: str,
                writer.writerow([question, answer["answer"]])
                print(f"Processed question: {question}, answer: {answer['answer']}")
    
    return {"message": f"Answers generated and saved to '{answers_file}'"}
