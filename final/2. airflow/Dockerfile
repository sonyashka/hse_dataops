FROM apache/airflow:2.8.1-python3.11

# Переключение на root для установки системных пакетов
USER root

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Возвращаемся к пользователю airflow
USER airflow

# Создаем директории для DAGs, логов и плагинов
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins /opt/airflow/config

# Копируем DAGs
COPY dags/ /opt/airflow/dags/