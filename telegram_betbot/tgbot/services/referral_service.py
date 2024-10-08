import logging
import re

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from telegram_betbot.database import Database
from telegram_betbot.database.models import Referral
from telegram_betbot.tgbot.exeptions.admin import ReferralKeyUniqueError
from telegram_betbot.tgbot.exeptions.referral import (
    ReferralAlreadyRegisteredByYouError,
    ReferralAlreadyRegisteredError,
    ReferralInvalidError,
)


logger = logging.getLogger(__name__)


class ReferralService:
    def __init__(self, db: Database):
        self.db = db

    async def create_new_referral_keys(
        self,
        bookmaker_name: str,
        streamer_name: str,
        referral_keys: list[str],
    ) -> None:
        try:
            async with self.db.referral.session.begin():
                streamer, bookmaker = await self.db.referral.get_data_for_referal(
                    bookmaker_name=bookmaker_name,
                    streamer_name=streamer_name,
                )

                await self.db.referral.create_many_referrals_for_one_streamer_and_bm(
                    streamer_id=streamer.id,
                    bookmaker_id=bookmaker.id,
                    referral_keys=referral_keys,
                )

                logger.info("Referral keys created")

        except IntegrityError as exception:
            logger.error(exception)

            match = re.search(r"Key \(referral_key\)=\((\d+)\)", str(exception))
            if match:
                existing_referral_key = match.group(1)
                raise ReferralKeyUniqueError(existing_referral_key)
            raise ReferralKeyUniqueError

    async def check_and_create_referral(
        self,
        bookmaker_name: str,
        streamer_name: str,
        telegram_id: int,
        referral_key: str,
    ) -> bool:
        async with self.db.referral.session.begin():
            streamer, bookmaker, user = await self.db.referral.get_data_for_referal(
                bookmaker_name=bookmaker_name,
                streamer_name=streamer_name,
                telegram_id=telegram_id,
            )
            referral = await self.db.referral.get_by_where(
                whereclause=and_(
                    Referral.bookmaker_id == bookmaker.id,
                    Referral.streamer_id == streamer.id,
                    Referral.referral_key == referral_key,
                ),
                options=[joinedload(Referral.user)],
            )

            if referral and referral.user_id is not None:
                if referral.user.id == user.id:
                    raise ReferralAlreadyRegisteredByYouError
                else:
                    raise ReferralAlreadyRegisteredError

            if referral:
                referral.user_id = user.id
                return True
            else:
                raise ReferralInvalidError
