FROM python:3.13-slim

WORKDIR /app

COPY core ./core
COPY infra ./infra
COPY services/api-gateway ./services/api-gateway
COPY pyproject.toml uv.lock ./ 

ENV PYTHONPATH=/app/services/api-gateway/src:/app

RUN pip install uv && uv sync

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "api_gateway.app:app", "--host", "0.0.0.0", "--port", "8080"]