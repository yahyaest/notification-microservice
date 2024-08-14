#!/bin/bash

# Create or update .env file with provided environment variables

# echo "BASE_URL=${BASE_URL}" > /app/.env
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


###################################################
########## Fix Prisma Migrate Lock Error ##########
###################################################

##### ERROR #####

# root@af471755341a:/app# prisma migrate dev
# Environment variables loaded from .env
# Prisma schema loaded from prisma/schema.prisma
# Datasource "db": PostgreSQL database "notification", schema "public" at "postgres:5432"

# Error: P1002

# The database server at `postgres`:`5432` was reached but timed out.

# Please try again.

# Please make sure your database server is running at `postgres`:`5432`.

# Context: Timed out trying to acquire a postgres advisory lock (SELECT pg_advisory_lock(72707369)). Elapsed: 10000ms. See https://pris.ly/d/migrate-advisory-locking for details.

##### Fix #####

## https://stackoverflow.com/questions/76450818/supabase-prisma-migrate-dev-sometimes-times-out-postgres-advisory-lock

# Prisma uses a PostgreSQL advisory lock with the magic number ID 72707369 that blocks a new migration if the previous one is still connected and idle.
# ---> This will happen if changes are made to schema.prisma file then restart the container without running prisma migrate dev command manually.In this case the entrypoint.sh file will run the prisma migrate dev command that ask for prompt and hang in there so the lock will not be resolved.


# yahya@yahya-debian ~/Projects/market-place-app $ docker exec -it postgres psql -U postgres -d notification
# notification=# SELECT pg_terminate_backend(PSA.pid)
# FROM pg_locks AS PL
#     INNER JOIN pg_stat_activity AS PSA ON PSA.pid = PL.pid
# WHERE PSA.state LIKE 'idle'
#     AND PL.objid IN (72707369);
#  pg_terminate_backend 
# ----------------------
#  t
# (1 row)