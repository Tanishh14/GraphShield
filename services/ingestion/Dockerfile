FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 ingestuser

COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn pydantic pytest

COPY . /app/
USER ingestuser

EXPOSE 8001

CMD ["python", "-m", "src.main"]
