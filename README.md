# QA-system

QA-system — это backend-сервис вопросно-ответной системы на базе языковой модели. Проект реализует чат-бота-консультанта для платформы онлайн-образования: пользователь задает вопрос о курсах, форматах обучения, преподавателях или условиях платформы, а система ищет релевантную информацию в базе знаний и генерирует ответ.

## Что делает проект

- принимает вопросы пользователя через REST API;
- строит embedding для текста вопроса;
- ищет похожие фрагменты знаний в Elasticsearch;
- передает найденный контекст в LLM;
- возвращает ответ, основанный на найденной информации;
- сохраняет историю вопросов и ответов в CSV-файл;
- позволяет загружать новые фрагменты знаний в индекс Elasticsearch;
- умеет генерировать ответы на набор тестовых вопросов для оценки качества.

## Архитектура

Проект построен как FastAPI-приложение и состоит из трех основных частей:

- `routes/main` — основной сценарий работы чат-бота: получить вопрос, найти контекст, сгенерировать ответ и сохранить историю.
- `routes/elastic_search` — API для работы с Elasticsearch: создание индекса, добавление и удаление документов, векторный поиск.
- `routes/llm` — API для работы с моделями: получение embeddings и генерация ответа через Ollama.

Общий поток обработки вопроса:

1. Клиент отправляет вопрос в `/main/get_answer`.
2. Сервис получает embedding вопроса с помощью модели `jinaai/jina-embeddings-v3`.
3. Elasticsearch выполняет kNN-поиск по embedding и возвращает наиболее релевантные фрагменты из базы знаний.
4. Найденные фрагменты передаются в языковую модель `hdnh2006/salamandra-2b-instruct:Q5_1`.
5. Модель формирует ответ на основе переданного контекста.
6. Вопрос и ответ сохраняются в `chat_history.csv`.

## Структура проекта

```text
.
├── Dockerfile
├── README.md
├── requirements.txt
└── src
    ├── main.py
    ├── questions.txt
    ├── answers.csv
    ├── topics.txt
    ├── chat_history.csv
    ├── configs
    │   ├── configuration_parser.py
    │   ├── http_ca.crt
    │   └── secrets.ini
    └── routes
        ├── elastic_search
        │   ├── routes.py
        │   └── types.py
        ├── llm
        │   ├── routes.py
        │   └── types.py
        └── main
            ├── routes.py
            └── types.py
```

## Основные файлы

- `src/main.py` — точка входа FastAPI-приложения.
- `src/routes/main/routes.py` — основной API чат-бота.
- `src/routes/elastic_search/routes.py` — маршруты для работы с Elasticsearch.
- `src/routes/llm/routes.py` — маршруты для embeddings и генерации ответа.
- `src/topics.txt` — база знаний о курсах и платформе.
- `src/questions.txt` — тестовые вопросы.
- `src/answers.csv` — ответы, сгенерированные для тестовых вопросов.
- `src/chat_history.csv` — история диалогов.
- `src/configs/secrets.ini` — конфигурация с секретами, например пароль Elasticsearch.
- `src/configs/http_ca.crt` — сертификат для подключения к Elasticsearch.

## Зависимости

Основные технологии:

- Python 3.11
- FastAPI
- Uvicorn
- Elasticsearch
- Ollama
- Transformers
- PyTorch
- `jinaai/jina-embeddings-v3` для embeddings
- `hdnh2006/salamandra-2b-instruct:Q5_1` для генерации ответов

Полный список Python-зависимостей находится в `requirements.txt`.

## Запуск через Docker

Соберите образ:

```bash
docker build -t qa-system .
```

Запустите контейнер:

```bash
docker run -p 8000:8000 qa-system
```

После запуска API будет доступно по адресу:

```text
http://localhost:8000
```

Документация FastAPI:

```text
http://localhost:8000/docs
```

## Локальный запуск

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите приложение из директории `src`:

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```

Для корректной работы также должны быть доступны:

- запущенный Elasticsearch на `https://localhost:9200`;
- сертификат `configs/http_ca.crt`;
- файл `configs/secrets.ini` с паролем Elasticsearch;
- установленный и запущенный Ollama.

## Основные API

### Получить ответ на вопрос

```http
POST /main/get_answer?index=<index_name>
```

Тело запроса:

```json
{
  "text": "Какие бесплатные курсы есть на платформе?"
}
```

### Добавить фрагмент знаний

```http
POST /main/add_topic?index=<index_name>
```

Тело запроса:

```json
{
  "text": "Название курса: ..."
}
```

### Загрузить фрагменты знаний из файла

```http
POST /main/load_topics?index=<index_name>&file_path=topics.txt
```

### Сгенерировать ответы на тестовые вопросы

```http
POST /main/generate_answers?index=<index_name>
```

По умолчанию вопросы берутся из `questions.txt`, а ответы сохраняются в `answers.csv`.

## Назначение

Проект можно использовать как прототип RAG-системы для консультаций по образовательной платформе. Он демонстрирует связку FastAPI, Elasticsearch, embedding-модели и локальной LLM через Ollama для генерации ответов на основе ограниченной базы знаний.
