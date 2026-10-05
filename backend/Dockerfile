FROM python:3.11.4-slim

LABEL authors="Abdulqadir Abuharrus"

WORKDIR /app
# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN uv pip install --system --index-url https://download.pytorch.org/whl/cpu \ transformers torch accelerate pillow fastapi uvicorn

# Download model at build time (~7GB, cached in Docker layers)
RUN python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
    AutoModelForCausalLM.from_pretrained('vikhyatk/moondream2', trust_remote_code=True); \
    AutoTokenizer.from_pretrained('vikhyatk/moondream2')"

# Copy app code
COPY . .

# Run single worker CPU bound anyway...
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
