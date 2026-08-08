FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 mluser

COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn pydantic pytest torch torch-geometric

COPY . /app/
USER mluser

EXPOSE 8002

CMD ["python", "-m", "src.serve"]
