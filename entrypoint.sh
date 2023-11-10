#!/bin/bash

# Wait for the PostgreSQL database to be ready
# until nc -z -v -w30 postgres 5432
# do
#   echo "Waiting for PostgreSQL to start..."
#   sleep 1
# done

# Run Prisma migrations
prisma migrate dev
prisma generate

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --reload --port 8000
