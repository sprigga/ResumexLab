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
# The migration file uses CREATE TABLE IF NOT EXISTS for idempotent migrations
# This allows safe re-running even if tables already exist
alembic upgrade head

echo "=== Migration Complete ==="
echo "=== Starting Application ==="

# Execute the main command (uvicorn)
exec "$@"
