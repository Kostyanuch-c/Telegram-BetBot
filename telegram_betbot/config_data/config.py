from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine import URL


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: str
    user: str
    passwd: str | None
    port: int
    host: str
    driver: str = "asyncpg"
    database_system: str = "postgresql"

    @staticmethod
    def from_env(env: Env) -> "DatabaseConfig":
        return DatabaseConfig(
            name=env.str("POSTGRES_DATABASE", "mydb"),
            user=env.str("POSTGRES_USER", "user"),
            passwd=env.str("POSTGRES_PASSWORD", None),
            port=env.int("POSTGRES_PORT", 5432),
            host=env.str("POSTGRES_HOST", "db"),
        )

    def build_connection_str(self) -> str:
        """This function builds a connection string."""
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            password=self.passwd,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


@dataclass
class TgBot:
    token: str


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int
    host: str
    port: int
    passwd: str | None
    username: str | None
    state_ttl: int | None
    data_ttl: int | None

    @staticmethod
    def from_env(env: Env) -> "RedisConfig":
        return RedisConfig(
            db=env.int("REDIS_DATABASE", 1),
            host=env.str("REDIS_HOST", "redis"),
            port=env.int("REDIS_PORT", 6379),
            passwd=env.str("REDIS_PASSWORD", None),
            username=env.str("REDIS_USERNAME", None),
            state_ttl=env.int("REDIS_TTL_STATE", None),
            data_ttl=env.int("REDIS_TTL_DATA", None),
        )


@dataclass
class Config:
    debug: bool
    logging_level: int
    tg_bot: TgBot
    redis: RedisConfig
    database: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        debug=env.bool("DEBUG"),
        logging_level=env.int("LOGGING_LEVEL"),
        redis=RedisConfig.from_env(env),
        database=DatabaseConfig.from_env(env),
    )
