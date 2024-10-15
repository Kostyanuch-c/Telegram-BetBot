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
	docker compose up --build --force-recreate

.PHONY: init_dump
init_dump:
	docker compose exec db pg_restore -U $$POSTGRES_USER -d $$POSTGRES_DB /app/init_dump.sql --verbose

.PHONY: rebuild-clean
rebuild-clean:
	docker compose down -v --remove-orphans
	docker compose up --build --force-recreate