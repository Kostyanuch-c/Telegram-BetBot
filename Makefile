DC = docker compose
DCE = docker compose exec
EXEC = docker exec -it
LOGS = docker logs
APP_CONTAINER = telegram-betbot
REDIS_CONTAINER = redis
POSTGRES_CONTAINER = db

.env:
	test ! -f .env && cp .env.example .env

.PHONY: lint
lint:
	@poetry run flake8 telegram_betbot

.PHONY: install-dependencies
install-dependencies: .env
	@poetry install

.PHONY: build
build:
	@poetry install --only main

setup-pre-commit-hooks:
	@poetry run pre-commit install

.PHONY: generate
install: install-dependencies setup-pre-commit-hooks

# Alembic utils
.PHONY: generate
generate:
	poetry run alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

# Docker utils
.PHONY: project-start
project-start:
	docker compose up --force-recreate ${MODE}

.PHONY: project-stop
project-stop:
	docker compose down --remove-orphans ${MODE}

.PHONY: build-recreate
build-recreate:
	${DC} up --build --force-recreate

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: db-logs
db-logs:
	${LOGS} ${POSTGRES_CONTAINER} -f

.PHONY: redis-logs
redis-logs:
	${LOGS} ${REDIS_CONTAINER} -f

.PHONY: docker-generate-migrate
docker-generate-migrate:
	${EXEC} ${APP_CONTAINER} poetry run alembic revision --m="$(NAME)"

.PHONY: docker-migrate
docker-migrate:
	${EXEC} ${APP_CONTAINER} poetry run alembic upgrade head

.PHONY: init_dump
POSTGRES_USER ?= user
POSTGRES_DB ?= mydb
init_dump:
	${EXEC} ${POSTGRES_CONTAINER} pg_restore -U $(POSTGRES_USER) -d $(POSTGRES_DB) --data-only /app/init_dump.sql --verbose

.PHONY: init_db
init_db: NAME ?= initial_migration
init_db: docker-generate-migrate docker-migrate init_dump