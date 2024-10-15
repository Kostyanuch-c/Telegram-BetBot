from collections.abc import Sequence
from typing import Any, cast

from sqlalchemy import (
    Row,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from telegram_betbot.database.models import (
    Bookmaker,
    Referral,
    Streamer,
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
            referral_key: int,
            telegram_id: int,
            is_confirmed: bool = False,
    ) -> None:
        referral = Referral(
            bookmaker_id=bookmaker_id,  # type: ignore[call-arg]
            streamer_id=streamer_id,  # type: ignore[call-arg]
            referral_key=referral_key,  # type: ignore[call-arg]
            user_telegram_id=telegram_id,  # type: ignore[call-arg]
            is_confirmed=is_confirmed,  # type: ignore[call-arg]
        )
        self.session.add(referral)

    async def get_data_for_referal(
            self,
            streamer_name: str,
            bookmaker_name: str,
            telegram_id: int = None,
    ) -> Row[tuple[Any, ...] | Any] | None:
        query = (
            select(Streamer.id, Bookmaker.id)
            .join(Bookmaker, cast("ColumnElement[bool]", Bookmaker.name == bookmaker_name))
            .where(cast("ColumnElement[bool]", Streamer.name == streamer_name))
            .where(cast("ColumnElement[bool]", Bookmaker.name == bookmaker_name))
        )

        result = await self.session.execute(query)

        return result.one_or_none()

    async def update_confirmed_status(
            self,
            streamer_id: int,
            bookmaker_id: int,
            referral_keys: list[int] | set[int],
    ) -> None:
        query = (
            update(Referral)
            .where(
                (Referral.bookmaker_id == bookmaker_id)
                & (Referral.streamer_id == streamer_id)
                & Referral.referral_key.in_(referral_keys),
            )
            .values(is_confirmed=True)
        )

        await self.session.execute(query)

    async def get_free_bookmakers_for_referral(self, telegram_id: int) -> tuple[dict, list]:
        referrals: Sequence[Referral] = await self.get_many(
            whereclause=Referral.user_telegram_id == telegram_id,
            options=[joinedload(Referral.bookmaker), joinedload(Referral.streamer)],
        )

        occupied_bookmakers = {
            ref.bookmaker.name: [ref.streamer.name, ref.is_confirmed] for ref in referrals
        }

        all_bookmakers = await self.session.execute(select(Bookmaker.id, Bookmaker.name))

        occupied_bookmaker_ids = {ref.bookmaker_id for ref in referrals}

        free_bookmakers = [
            bookmaker_name
            for bookmaker_id, bookmaker_name in all_bookmakers
            if bookmaker_id not in occupied_bookmaker_ids
        ]

        return occupied_bookmakers, free_bookmakers
