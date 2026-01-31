#!/bin/bash
# Entrypoint script for Resume Management System Backend
# Created: 2025-01-31
# Purpose: Handle database migrations and start the application

set -e

echo "=== Starting Backend Entrypoint ==="

# Wait a moment for filesystem to be ready
sleep 1

echo "=== Running Alembic Migrations ==="

# Run alembic upgrade to head
# The migration files include column existence checks to handle idempotent migrations
alembic upgrade head

echo "=== Migration Complete ==="
echo "=== Starting Application ==="

# Execute the main command (uvicorn)
exec "$@"
