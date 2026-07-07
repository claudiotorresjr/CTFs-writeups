FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/pyproject.toml src/uv.lock* ./

ENV HOME=/app

RUN uv sync --locked; \
    uv run playwright install --with-deps chromium

COPY ./run.sh .
RUN chmod +x run.sh
COPY src/ ./src/

EXPOSE 5000

ENTRYPOINT ["/app/run.sh"]
