FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

WORKDIR /code/
COPY Pipfile Pipfile.lock ./


RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . /code/
EXPOSE 8000