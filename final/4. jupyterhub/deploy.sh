#!/bin/bash

echo "Starting JupyterHub deployment..."

# Создание необходимых директорий
mkdir -p jupyterhub_data users

# Генерация секретного ключа если не задан в .env
if ! grep -q "JUPYTERHUB_CRYPT_KEY=" .env; then
    echo "JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)" >> .env
fi

# Создание системных пользователей (требует sudo)
echo "Creating system users..."
chmod +x create_users.sh
./create_users.sh

# Сборка и запуск контейнера
echo "Building and starting JupyterHub container..."
docker-compose up -d --build

# Ожидание запуска
echo "Waiting for JupyterHub to start..."
sleep 10

# Проверка статуса
echo "Checking container status..."
docker-compose ps

echo ""
echo "JupyterHub should be available at: http://localhost:8000"
echo "Login with: admin / admin123"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"