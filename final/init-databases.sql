-- Создание баз данных если они не существуют
CREATE DATABASE mlflow_db;
CREATE DATABASE airflow_db;

-- Создание пользователей
CREATE USER mlflow_user WITH PASSWORD 'mlflow_password123';
CREATE USER airflow_user WITH PASSWORD 'airflow_password123';

-- Назначение прав
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

-- Даем права на схему public для пользователей
\c mlflow_db
GRANT ALL ON SCHEMA public TO mlflow_user;

\c airflow_db
GRANT ALL ON SCHEMA public TO airflow_user;