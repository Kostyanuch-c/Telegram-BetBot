import logging

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine as _create_async_engine,
)

from telegram_betbot.database.repositories import ReferralRepo
from telegram_betbot.database.repositories.streamers_and_bookmakers import StreamerBookmakerRepo
from telegram_betbot.database.repositories.user import UserRepo


logger = logging.getLogger(__name__)


def create_async_engine(url: URL | str, echo: bool = False) -> AsyncEngine:
    """Create async engine with given URL.

    :param echo:
    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=echo, pool_pre_ping=True)


class Database:
    user: UserRepo
    """ User repository """
    referral: ReferralRepo
    """ Referral repository """
    streamers_and_bookmakers: StreamerBookmakerRepo
    """ Streamer referral link repository """
    """ Chat repository """
    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        referral: ReferralRepo = None,
        streamers_and_bookmakers: StreamerBookmakerRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param user: (Optional) User repository
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.referral = referral or ReferralRepo(session=session)
        self.streamers_and_bookmakers = streamers_and_bookmakers or StreamerBookmakerRepo(
            session=session,
        )
