FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV TZ=Europe/Minsk

CMD ["python", "main.py"]
