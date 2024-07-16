FROM python:3.10-bullseye

USER root

RUN apt update -y
RUN apt install nmap -y

RUN pip install --upgrade pip

RUN mkdir /api
WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /api/app


CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]