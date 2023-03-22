#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# Start server
echo "Starting server"
poetry run uvicorn task_admin.app:app --host 0.0.0.0 --port 8000