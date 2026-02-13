FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY src ./src

RUN pip install uv && uv sync

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "api_gateway.app:app", "--host", "0.0.0.0", "--port", "8080"]