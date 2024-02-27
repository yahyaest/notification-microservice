#!/bin/bash

# Create or update .env file with provided environment variables

# echo "GATEWAY_BASE_URL=${GATEWAY_BASE_URL}" > /app/.env
# echo "LOG_LEVEL=${LOG_LEVEL}" >> /app/.env
# echo "DATABASE_URL=${DATABASE_URL}" >> /app/.env
# echo "JWT_SECRET=${JWT_SECRET}" >> /app/.env

# Add dynamically passed environment variables to .env file
# Empty .env file
> /app/.env
for line in $(env); do
  echo "$line" >> /app/.env
done

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
