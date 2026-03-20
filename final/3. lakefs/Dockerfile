FROM treeverse/lakefs:latest

USER root

# Установка PostgreSQL клиента и других утилит
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Создание скрипта запуска
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Создание директории для конфигурации
RUN mkdir -p /home/lakefs/.lakefs && chown -R lakefs:lakefs /home/lakefs/.lakefs

USER lakefs

ENTRYPOINT ["/start.sh"]