FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка MLflow и зависимостей
RUN pip install --no-cache-dir \
    mlflow>=2.8.0 \
    psycopg2-binary \
    boto3

# Создание директории для артефактов
RUN mkdir -p /mlflow/artifacts

# Копируем скрипт ожидания из той же директории, что и Dockerfile
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Открываем порт для MLflow
EXPOSE 5000

# Скрипт будет запущен с аргументом "postgres" (хост БД)
ENTRYPOINT ["/wait-for-db.sh"]