# Telegram-BetBot
<a href="https://codeclimate.com/github/Kostyanuch-c/Telegram-BetBot/maintainability"><img src="https://api.codeclimate.com/v1/badges/b64d98eb84c5e0cdca7a/maintainability" /></a>
[![Docker CI/CD](https://github.com/Kostyanuch-c/Telegram-BetBot/actions/workflows/automation.yml/badge.svg)](https://github.com/Kostyanuch-c/Telegram-BetBot/actions/workflows/automation.yml)
[![Flake8](https://github.com/Kostyanuch-c/Telegram-BetBot/actions/workflows/flake8.yaml/badge.svg)](https://github.com/Kostyanuch-c/Telegram-BetBot/actions/workflows/flake8.yaml)

## Technologies

This project uses the following dependencies:

```toml
[tool.poetry.dependencies]
python = "^3.10"
aiogram = "^3.13.1"
alembic = "^1.13.3"
environs = "^11.0.0"
redis = "^5.1.1"
asyncpg = "^0.29.0"
sqlalchemy = "^2.0.35"
aiogram-dialog = "^2.2.0"
```

## Running with Docker

To run the bot using Docker, execute the following commands:

1. Create the `.env` file (if you haven't done so already):
   
   **Edit the `.env` file and insert your bot token, other variables can remain unchanged.**
   ```bash
   make .env
   ```

2. Start the project:

   ```bash
   make project-start
   ```

3. Initialize the database. **Only for the first run!**:

   ```bash
   make init_db
   ```

After the first run, use the migration commands:

- To generate a new migration:

   ```bash
   make docker-generate-migrate NAME="your_migration_name"
   ```

- To apply migrations:

   ```bash
   make docker-migrate
   ```

## Makefile Commands

- `.env`: Copies the `.env.example` file to `.env` if it doesn't exist.
- `project-start`: Starts the project using Docker.
- `project-stop`: Stops the project and removes orphaned containers.
- `build-recreate`: Rebuilds the Docker images and recreates the containers.
- `app-logs`: Displays logs for the application container in real-time.
- `db-logs`: Displays logs for the PostgreSQL container in real-time.
- `redis-logs`: Displays logs for the Redis container in real-time.
- `docker-generate-migrate`: Generates a new Alembic migration with a specified name.
- `docker-migrate`: Applies the database migrations using Alembic. 

