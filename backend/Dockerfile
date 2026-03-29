FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# catboost runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

# Support both build contexts:
# 1) repo root (contains /backend)
# 2) /backend as service root directory
COPY . /src
RUN set -eux; \
    if [ -f /src/backend/requirements.txt ]; then \
      cp /src/backend/requirements.txt /app/requirements.txt; \
      cp -R /src/backend/. /app/; \
    else \
      cp /src/requirements.txt /app/requirements.txt; \
      cp -R /src/. /app/; \
    fi; \
    pip install --upgrade pip; \
    pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
