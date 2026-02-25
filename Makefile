include .env
export

GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

VENV_NAME := venv
VENV_BIN := $(VENV_NAME)/bin
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
YOYO := $(VENV_BIN)/yoyo

$(VENV_NAME):
	@echo "$(YELLOW)Создание виртуального окружения...$(NC)"
	python3 -m venv $(VENV_NAME)
	@echo "$(GREEN)✓ Виртуальное окружение создано$(NC)"

.PHONY: dev.install
dev.install: $(VENV_NAME)
	@echo "$(YELLOW)Установка зависимостей...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Зависимости установлены$(NC)"

.PHONY: db.start
db.start:
	@echo "$(YELLOW)Запуск PostgreSQL через Docker...$(NC)"
	docker-compose up -d db
	@echo "$(GREEN)✓ PostgreSQL запущен$(NC)"

.PHONY: db.stop
db.stop:
	@echo "$(YELLOW)Остановка PostgreSQL...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ PostgreSQL остановлен$(NC)"

.PHONY: db.migration.new
db.migration.new:
	@echo "$(YELLOW)Создание новой миграции: $(name)$(NC)"
	@cd migrations && $(YOYO) new --editor=vi "$(name)"
	@echo "$(GREEN)✓ Миграция создана. Отредактируйте файл в migrations/$(NC)"
	@echo "$(YELLOW)Используйте :wq! для выхода из vim$(NC)"

.PHONY: db.migrate
db.migrate:
	@echo "$(YELLOW)Применение миграций к базе данных...$(NC)"
	$(YOYO) apply --database "$(DB_URL)" migrations/
	@echo "$(GREEN)✓ Миграции применены$(NC)"

.PHONY: db.rollback
db.rollback:
	@echo "$(YELLOW)Откат последней миграции...$(NC)"
	$(YOYO) rollback --database "$(DB_URL)" migrations/ --one
	@echo "$(GREEN)✓ Миграция откатана$(NC)"

.PHONY: db.rollback.all
db.rollback.all:
	@echo "$(YELLOW)Откат всех миграций...$(NC)"
	$(YOYO) rollback --database "$(DB_URL)" migrations/ --all
	@echo "$(GREEN)✓ Все миграции откатаны$(NC)"

.PHONY: db.status
db.status:
	@echo "$(YELLOW)Статус миграций:$(NC)"
	$(YOYO) status --database "$(DB_URL)" migrations/

.PHONY: db.recreate
db.recreate: db.rollback.all db.migrate
	@echo "$(GREEN)✓ База данных пересоздана$(NC)"

.PHONY: clean
clean:
	@echo "$(YELLOW)Очистка проекта...$(NC)"
	rm -rf $(VENV_NAME)
	rm -rf __pycache__
	rm -rf *.pyc
	@echo "$(GREEN)✓ Проект очищен$(NC)"

.PHONY: help
help:
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo "  make dev.install              - Установка зависимостей"
	@echo "  make db.start                  - Запуск PostgreSQL в Docker"
	@echo "  make db.stop                   - Остановка PostgreSQL"
	@echo "  make db.migration.new name=... - Создание новой миграции"
	@echo "  make db.migrate                 - Применение миграций"
	@echo "  make db.rollback                - Откат последней миграции"
	@echo "  make db.rollback.all            - Откат всех миграций"
	@echo "  make db.status                   - Статус миграций"
	@echo "  make db.recreate                 - Пересоздание БД"
	@echo "  make clean                       - Очистка проекта"