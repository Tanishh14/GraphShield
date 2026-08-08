FROM python:3.11-slim

WORKDIR /app

# Non-root user setup
RUN useradd -m -u 1000 apiuser

COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn pydantic pytest httpx

COPY . /app/
USER apiuser

EXPOSE 8000

CMD ["python", "-m", "src.main"]
