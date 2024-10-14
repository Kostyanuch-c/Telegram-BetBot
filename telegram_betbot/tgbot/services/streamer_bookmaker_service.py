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
        bookmaker_id: int,
        streamer_id: int,
        referral_link: str,
    ) -> None:
        async with self.db.streamers_and_bookmakers.session.begin():
            await self.db.streamers_and_bookmakers.update_or_create(
                streamer_id=streamer_id,
                bookmaker_id=bookmaker_id,
                referral_link=referral_link,
            )

            logger.info("Referral links updated")

    async def get_referral_link(self, bookmaker_id: int, streamer_id: int) -> str:
        async with self.db.streamers_and_bookmakers.session.begin():
            link = await self.db.streamers_and_bookmakers.get_by_where(
                whereclause=and_(
                    StreamerBookmakerMembership.bookmaker_id == bookmaker_id,
                    StreamerBookmakerMembership.streamer_id == streamer_id,
                ),
            )

            return link.referral_link
