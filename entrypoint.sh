#!/bin/bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting server..."
exec gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
