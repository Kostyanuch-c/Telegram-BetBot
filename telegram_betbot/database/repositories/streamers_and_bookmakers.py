from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database.models import (
    Bookmaker,
    Streamer,
    StreamerBookmakerMembership,
)
from telegram_betbot.database.repositories.abstract import Repository


class StreamerBookmakerRepo(Repository[StreamerBookmakerMembership]):
    """StreamerBookmaker repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=StreamerBookmakerMembership, session=session)

    async def update_or_create(
        self,
        bookmaker_id: int,
        streamer_id: int,
        referral_link: str,
    ) -> None:
        stmt = (
            update(StreamerBookmakerMembership)
            .where(
                StreamerBookmakerMembership.bookmaker_id == bookmaker_id,
                StreamerBookmakerMembership.streamer_id == streamer_id,
            )
            .values(referral_link=referral_link)
        )
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            new_entry = StreamerBookmakerMembership(
                bookmaker_id=bookmaker_id,  # type: ignore[call-arg]
                streamer_id=streamer_id,  # type: ignore[call-arg]
                referral_link=referral_link,  # type: ignore[call-arg]
            )
            await self.session.merge(new_entry)

    async def get_data_bookmaker_and_streamer(
        self,
        streamer_name: str,
        bookmaker_name: str,
    ) -> tuple:
        query = (
            select(Streamer, Bookmaker)
            .join(Bookmaker, Bookmaker.name == bookmaker_name)
            .where(Streamer.name == streamer_name)
        )

        result = await self.session.execute(query)

        return result.fetchone()
