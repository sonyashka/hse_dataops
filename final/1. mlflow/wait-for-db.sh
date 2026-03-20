#!/bin/bash
set -e

# Ожидаем PostgreSQL
host="$1"
shift
cmd="$@"

echo "Waiting for PostgreSQL at $host..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - starting MLflow server"

# Запускаем MLflow сервер
exec mlflow server \
    --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB \
    --default-artifact-root file:///mlflow/artifacts \
    --host 0.0.0.0 \
    --port 5000