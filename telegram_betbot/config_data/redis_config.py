from dataclasses import dataclass

from environs import Env
from redis.asyncio.client import Redis


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


async def create_redis_connection(redis_config: RedisConfig) -> Redis:
    redis = Redis(
        host=redis_config.host,
        port=redis_config.port,
        password=redis_config.passwd,
        db=redis_config.db,
    )
    return redis
