FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy dependency specifications first for Docker cache optimization
COPY pyproject.toml poetry.lock ./

# Install project dependencies without trying to build the project root as a wheel
RUN poetry install --no-root --without dev

# Copy application source code
COPY . .

# Render exposes the port dynamically via $PORT
ENV PORT=10000
EXPOSE 10000

# Start command
CMD ["sh", "-c", "uvicorn src.app.app:app --host 0.0.0.0 --port ${PORT}"]

