FROM python:3.12-slim AS base
LABEL authors="Abdulqadir Abuharrus"
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock uv.toml ./

RUN uv sync --system --no-dev
# Download model at build time (~7GB, cached in Docker layers)
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
    AutoModelForCausalLM.from_pretrained('vikhyatk/moondream2', trust_remote_code=True); \
    AutoTokenizer.from_pretrained('vikhyatk/moondream2')"

COPY . .

ENV HF_HUB_DISABLE_TELEMETRY=1

EXPOSE 8000
# Run single worker CPU bound anyway...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
