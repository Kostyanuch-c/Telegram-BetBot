"""Mocked Database."""
from sqlalchemy import MetaData

from telegram_betbot.database import Database
from telegram_betbot.database.models import Base


class MockedDatabase(Database):
    """Mocked database is used for integration tests."""

    async def teardown(self):
        """Clear all data in the database."""
        metadata: MetaData = Base.metadata  # noqa
        for table in metadata.sorted_tables:
            await self.session.execute(table.delete())
        await self.session.commit()
