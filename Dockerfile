FROM ubuntu

FROM python:3.11.1

RUN pip install --upgrade pip

WORKDIR /app

COPY /requirements.txt ./

RUN pip install -r requirements.txt

COPY /src /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]