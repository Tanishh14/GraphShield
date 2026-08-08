FROM python:3.11-slim

WORKDIR /app

# Non-root user setup
RUN useradd -m -u 1000 agentuser

COPY pyproject.toml /app/
RUN pip install --no-cache-dir pydantic langgraph pytest

COPY . /app/
USER agentuser

CMD ["python", "-m", "src.main"]
