import logging
from collections.abc import Sequence

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from telegram_betbot.database import Database
from telegram_betbot.database.entities.referral import ReferralEntity
from telegram_betbot.database.models import Referral
from telegram_betbot.tgbot.exeptions.admin import ReferralUpdateStatusError
from telegram_betbot.tgbot.exeptions.referral import ReferralAlreadyRegisteredError


logger = logging.getLogger(__name__)


class ReferralService:
    def __init__(self, db: Database):
        self.db = db

    async def update_referral_status(
        self,
        bookmaker_id: int,
        streamer_id: int,
        referral_keys: list[int] | set[int],
    ) -> None:
        try:
            async with self.db.referral.session.begin():
                await self.db.referral.update_confirmed_status(
                    streamer_id=streamer_id,
                    bookmaker_id=bookmaker_id,
                    referral_keys=referral_keys,
                )

                logger.info("Referral status updated")

        except SQLAlchemyError as exception:
            logger.error(exception)
            raise ReferralUpdateStatusError(str(exception))

    async def check_and_create_referral(
        self,
        bookmaker_id: int,
        streamer_id: int,
        telegram_id: int,
        referral_key: int,
    ) -> None:
        try:
            async with self.db.referral.session.begin():
                await self.db.referral.create(
                    referral_key=referral_key,
                    bookmaker_id=bookmaker_id,
                    streamer_id=streamer_id,
                    telegram_id=telegram_id,
                )
        except IntegrityError as exception:
            logger.error(exception)
            raise ReferralAlreadyRegisteredError

    async def get_referrals_by_where(
        self,
        streamer_id: int,
        bookmaker_id: int,
        is_confirmed: bool = False,
    ) -> list[ReferralEntity]:
        async with self.db.referral.session.begin():
            refs: Sequence[Referral] = await self.db.referral.get_many(
                whereclause=and_(
                    Referral.streamer_id == streamer_id,
                    Referral.bookmaker_id == bookmaker_id,
                    Referral.is_confirmed.is_(is_confirmed),
                ),
            )
            return [
                ReferralEntity(
                    id=ref.id,
                    user_telegram_id=ref.user_telegram_id,
                    streamer_id=ref.streamer_id,
                    bookmaker_id=ref.bookmaker_id,
                    referral_key=ref.referral_key,
                    is_confirmed=ref.is_confirmed,
                )
                for ref in refs
            ]

    async def get_dara_for_referral(
        self,
        bookmaker_name: str,
        streamer_name: str,
    ) -> tuple[int, int]:
        async with self.db.referral.session.begin():
            streamer_id, bookmaker_id = await self.db.referral.get_data_for_referal(
                bookmaker_name=bookmaker_name,
                streamer_name=streamer_name,
            )

            return streamer_id, bookmaker_id

    async def check_free_bookmakers(self, telegram_id: int) -> tuple[dict, list]:
        async with self.db.referral.session.begin():
            return await self.db.referral.get_free_bookmakers_for_referral(
                telegram_id=telegram_id,
            )
