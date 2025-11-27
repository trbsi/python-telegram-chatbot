FROM python:3.14-slim

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY ../ .

RUN poetry install --no-interaction
