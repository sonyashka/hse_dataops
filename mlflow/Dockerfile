FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mlflow psycopg2-binary boto3

RUN mkdir -p /mlflow/artifacts

EXPOSE 5000

CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"]