from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from telegram_betbot.database.models import (
    Bookmaker,
    Referral,
    Streamer,
    User,
)
from telegram_betbot.database.repositories.abstract import Repository


class ReferralRepo(Repository[Referral]):
    """Referral repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Referral, session=session)

    async def create(
        self,
        bookmaker_id: int,
        streamer_id: int,
        referral_key: str,
        user_id: int | None = None,
        telegram_id: int | None = None,
    ) -> None:
        referral = Referral(
            bookmaker_id=bookmaker_id,  # type: ignore[call-arg]
            streamer_id=streamer_id,  # type: ignore[call-arg]
            referral_key=referral_key,  # type: ignore[call-arg]
            user_id=user_id,  # type: ignore[call-arg]
            telegram_id=telegram_id,  # type: ignore[call-arg]
        )
        await self.session.merge(referral)

    async def get_data_for_referal(
        self,
        streamer_name: str,
        bookmaker_name: str,
        telegram_id: int = None,
    ) -> tuple:
        query = (
            select(Streamer.id, Bookmaker.id)
            .select_from(Streamer)
            .join(Bookmaker, Bookmaker.name == bookmaker_name)
            .where(Streamer.name == streamer_name)
        )

        if telegram_id is not None:
            query = query.join(User, User.telegram_id == telegram_id).add_columns(User.id)

        result = await self.session.execute(query)

        return result.one_or_none()

    async def create_many_referrals_for_one_streamer_and_bm(
        self,
        streamer_id: int,
        bookmaker_id: int,
        referral_keys: list[str],
        user_id: int | None = None,
    ) -> None:
        referrals = [
            Referral(
                bookmaker_id=bookmaker_id,  # type: ignore[call-arg]
                streamer_id=streamer_id,  # type: ignore[call-arg]
                referral_key=referral_key,  # type: ignore[call-arg]
                user_id=user_id,  # type: ignore[call-arg]
            )
            for referral_key in referral_keys
        ]
        self.session.add_all(referrals)

    async def get_free_bookmakers_for_referral(self, telegram_id: int) -> tuple[dict, list]:
        referrals: list[Referral] = await self.get_many(
            whereclause=Referral.telegram_id == telegram_id,
            options=[joinedload(Referral.bookmaker), joinedload(Referral.streamer)],
        )

        occupied_bookmakers = {ref.bookmaker.name: ref.streamer.name for ref in referrals}

        all_bookmakers = await self.session.execute(select(Bookmaker.id, Bookmaker.name))

        occupied_bookmaker_ids = {ref.bookmaker_id for ref in referrals}

        free_bookmakers = [
            bookmaker_name
            for bookmaker_id, bookmaker_name in all_bookmakers
            if bookmaker_id not in occupied_bookmaker_ids
        ]

        return occupied_bookmakers, free_bookmakers
