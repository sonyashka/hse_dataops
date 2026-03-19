#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for PostgreSQL at $host for Airflow..."
until PGPASSWORD=$AIRFLOW_POSTGRES_PASSWORD psql -h "$host" -U "$AIRFLOW_POSTGRES_USER" -d "$AIRFLOW_POSTGRES_DB" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - executing command"
exec $cmd