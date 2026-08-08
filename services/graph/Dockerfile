FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 graphuser

COPY pyproject.toml /app/
RUN pip install --no-cache-dir pydantic pytest

COPY . /app/
USER graphuser

CMD ["python", "-m", "src.main"]
