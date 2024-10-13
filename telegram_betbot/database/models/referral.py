from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


if TYPE_CHECKING:
    from .bookmaker import Bookmaker
    from .streamer import Streamer
    from .user import User


class Referral(Base):
    """Referral model."""

    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id"),
        nullable=False,
    )
    bookmaker_id: Mapped[int] = mapped_column(
        ForeignKey("bookmakers.id"),
        nullable=False,
    )
    streamer_id: Mapped[int] = mapped_column(
        ForeignKey("streamers.id"),
        nullable=False,
    )

    referral_key: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    __table_args__ = (
        UniqueConstraint("user_telegram_id", "bookmaker_id", name="uq_user_bookmaker"),
    )

    bookmaker: Mapped["Bookmaker"] = relationship(
        "Bookmaker",
        back_populates="referrals",
    )
    streamer: Mapped["Streamer"] = relationship(
        "Streamer",
        back_populates="referrals",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="referrals",
    )
