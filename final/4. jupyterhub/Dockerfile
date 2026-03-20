FROM python:3.14-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Установка глобальных npm пакетов
RUN npm install -g configurable-http-proxy

# Установка Python пакетов
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterlab \
    notebook \
    jupyter-server-proxy

# Создание пользователя для JupyterHub
RUN useradd -m -s /bin/bash jupyter && \
    mkdir -p /home/jupyter/.jupyter && \
    chown -R jupyter:jupyter /home/jupyter

# Создание директории для конфигурации
RUN mkdir -p /etc/jupyterhub && \
    chown -R jupyter:jupyter /etc/jupyterhub

# Копирование конфигурационного файла
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

# Установка прав
RUN chown jupyter:jupyter /etc/jupyterhub/jupyterhub_config.py

# Создание директории для работы пользователей
RUN mkdir -p /home/jupyter/work && \
    chown -R jupyter:jupyter /home/jupyter/work

# Переключение на пользователя jupyter
USER jupyter
WORKDIR /home/jupyter

# Порт для JupyterHub
EXPOSE 8000

# Запуск JupyterHub
CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]