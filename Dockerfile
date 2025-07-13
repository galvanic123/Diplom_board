FROM python:3.12-slim


# 1. Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 2. Установка Poetry (официальный метод)
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

WORKDIR /app

# 4. Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# 5. Установка зависимостей (с отключением виртуального окружения)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# 6. Копирование остального кода
COPY . .