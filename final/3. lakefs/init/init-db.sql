-- Создание базы данных если не существует
SELECT 'CREATE DATABASE lakefs' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lakefs')\gexec

-- Создание пользователя если не существует
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'lakefs') THEN
      CREATE USER lakefs WITH PASSWORD 'lakefs123';
   END IF;
END
$$;

-- Предоставление прав
GRANT ALL PRIVILEGES ON DATABASE lakefs TO lakefs;
\c lakefs
GRANT ALL ON SCHEMA public TO lakefs;