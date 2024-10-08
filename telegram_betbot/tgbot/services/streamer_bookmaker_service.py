import logging

from sqlalchemy import and_

from telegram_betbot.database import Database
from telegram_betbot.database.models import StreamerBookmakerMembership


logger = logging.getLogger(__name__)


class StreamerBookmakerService:
    def __init__(self, db: Database):
        self.db = db

    async def update_or_create_referral_link(
        self,
        bookmaker_name: str,
        streamer_name: str,
        referral_link: str,
    ) -> None:
        async with self.db.streamers_and_bookmakers.session.begin():
            (
                streamer,
                bookmaker,
            ) = await self.db.streamers_and_bookmakers.get_data_bookmaker_and_streamer(
                bookmaker_name=bookmaker_name,
                streamer_name=streamer_name,
            )

            await self.db.streamers_and_bookmakers.update_or_create(
                streamer_id=streamer.id,
                bookmaker_id=bookmaker.id,
                referral_link=referral_link,
            )

            logger.info("Referral links updated")

    async def get_referral_link(self, bookmaker_name: str, streamer_name: str) -> str:
        async with self.db.streamers_and_bookmakers.session.begin():
            (
                streamer,
                bookmaker,
            ) = await self.db.streamers_and_bookmakers.get_data_bookmaker_and_streamer(
                bookmaker_name=bookmaker_name,
                streamer_name=streamer_name,
            )

            link = await self.db.streamers_and_bookmakers.get_by_where(
                whereclause=and_(
                    StreamerBookmakerMembership.bookmaker_id == bookmaker.id,
                    StreamerBookmakerMembership.streamer_id == streamer.id,
                ),
            )

            return link.referral_link
