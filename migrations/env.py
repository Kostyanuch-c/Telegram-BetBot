import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from sqlalchemy.exc import ProgrammingError
from alembic import context

from telegram_betbot.config_data.config import load_config
from telegram_betbot.database.models.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load your custom configuration
myconfig = load_config()

# Set the sqlalchemy.url from your configuration
config.set_main_option('sqlalchemy.url', myconfig.database.build_connection_str())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Run migrations in 'online' mode."""
    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )

    with context.begin_transaction():
        context.run_migrations()


class FailedConnectToDatabase(Exception):
    def __init__(self, url_info: str, other: Exception | str = ""):
        self.url_info = url_info
        self.other = other

    def __str__(self):
        return f"Tried to connect to {self.url_info} ({self.other})"


class MigrationError(Exception):
    def __init__(self, info: str):
        self.info = info

    def __str__(self):
        return self.info


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with an async engine."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        future=True,
    )
    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    except ProgrammingError as pe:
        raise MigrationError(str(pe))
    except Exception as e:
        raise FailedConnectToDatabase(url_info=connectable.url, other=e)
    finally:
        await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())