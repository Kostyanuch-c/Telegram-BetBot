import logging
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from telegram_betbot.database import Database
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
        referral_keys: list[int],
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
        bookmaker_name: str,
        streamer_name: str,
        telegram_id: int,
        referral_key: int,
    ) -> None:
        try:
            async with self.db.referral.session.begin():
                streamer_id, bookmaker_id = await self.db.referral.get_data_for_referal(
                    bookmaker_name=bookmaker_name,
                    streamer_name=streamer_name,
                    telegram_id=telegram_id,
                )
                await self.db.referral.create(
                    referral_key=referral_key,
                    bookmaker_id=bookmaker_id,
                    streamer_id=streamer_id,
                    telegram_id=telegram_id,
                )
        except IntegrityError as exception:
            logger.error(exception)
            raise ReferralAlreadyRegisteredError

    async def check_free_bookmakers(self, telegram_id: int) -> tuple[dict, list]:
        async with self.db.referral.session.begin():
            return await self.db.referral.get_free_bookmakers_for_referral(
                telegram_id=telegram_id,
            )

    async def get_referrals_id_by_bm_and_streamer(
        self,
        streamer_id: int,
        bookmaker_id: int,
    ) -> Sequence[int]:
        async with self.db.referral.session.begin():
            refs = await self.db.referral.get_ids_refs_by_streamer_name_and_bm_name(
                streamer_id=streamer_id,
                bookmaker_id=bookmaker_id,
            )
            return refs

    async def get_referrals_telegram_id(
        self,
        streamer_id: int,
        bookmaker_id: int,
    ) -> Sequence[int]:
        async with self.db.referral.session.begin():
            ref_telegram_id = await self.db.referral.get_refs_telegram_id(
                streamer_id=streamer_id,
                bookmaker_id=bookmaker_id,
            )
            return ref_telegram_id

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
