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