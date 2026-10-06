FROM python:3.12-slim
LABEL authors="Abdulqadir Abuharrus"
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock uv.toml ./

RUN uv sync --system --no-dev

COPY . .

ENV HF_HUB_DISABLE_TELEMETRY=1

EXPOSE 8000
# Run single worker CPU bound anyway...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
