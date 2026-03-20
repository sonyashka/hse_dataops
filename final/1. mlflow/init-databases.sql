-- Создание баз данных если они не существуют
CREATE DATABASE mlflow_db;

-- Создание пользователей
CREATE USER mlflow_user WITH PASSWORD 'mlflow_password123';

-- Назначение прав
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;

-- Даем права на схему public для пользователей
\c mlflow_db
GRANT ALL ON SCHEMA public TO mlflow_user;