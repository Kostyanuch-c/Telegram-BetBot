from dataclasses import dataclass

from environs import Env

from telegram_betbot.config_data.db_config import DatabaseConfig
from telegram_betbot.config_data.redis_config import RedisConfig


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    debug: bool
    tg_bot: TgBot
    redis: RedisConfig
    database: DatabaseConfig
    logging_level: int
    logging_format: str = (
        "[%(asctime)s] #%(levelname)-8s %(filename)s:" "%(lineno)d - %(name)s - %(message)s"
    )


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        debug=env.bool("DEBUG"),
        redis=RedisConfig.from_env(env),
        database=DatabaseConfig.from_env(env),
        logging_level=env.int("LOGGING_LEVEL"),
    )
