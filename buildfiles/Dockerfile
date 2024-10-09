FROM python:3.12-slim as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY ../poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-cache --no-root

COPY .. .

CMD ["poetry", "run", "python", "-m", "telegram_betbot.tgbot"]