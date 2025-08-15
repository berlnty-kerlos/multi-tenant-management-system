#!/bin/bash

# Wait for Postgres to be ready
echo "Waiting for Postgres..."
while ! pg_isready -h db -p ${POSTGRES_PORT} -U ${POSTGRES_USER}; do
  sleep 1
done

# Run Alembic migrations
alembic upgrade head

# Start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT} --reload
