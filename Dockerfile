FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"
ENV TZ=Europe/Minsk

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

CMD ["python", "-u", "main.py"]