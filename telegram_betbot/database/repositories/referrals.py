from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> None:
        referral = Referral(
            bookmaker_id=bookmaker_id,  # type: ignore[call-arg]
            streamer_id=streamer_id,  # type: ignore[call-arg]
            referral_key=referral_key,  # type: ignore[call-arg]
            user_id=user_id,  # type: ignore[call-arg]
        )
        await self.session.merge(referral)

    async def get_data_for_referal(
        self,
        streamer_name: str,
        bookmaker_name: str,
        telegram_id: int = None,
    ) -> tuple:
        query = (
            select(Streamer, Bookmaker)
            .select_from(Streamer)
            .join(Bookmaker, Bookmaker.name == bookmaker_name)
            .where(Streamer.name == streamer_name)
        )

        if telegram_id is not None:
            query = query.join(User, User.telegram_id == telegram_id).add_columns(User)

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
