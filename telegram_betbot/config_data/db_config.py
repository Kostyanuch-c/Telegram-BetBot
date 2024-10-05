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
