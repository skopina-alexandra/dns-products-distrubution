FROM python:3.13-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y netcat-traditional && \
    pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

COPY . /app
EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]