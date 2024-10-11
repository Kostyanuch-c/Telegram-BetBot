from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
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

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        default=None,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True,
        default=None,
    )
    bookmaker_id: Mapped[int] = mapped_column(
        ForeignKey("bookmakers.id"),
        nullable=False,
    )
    streamer_id: Mapped[int] = mapped_column(
        ForeignKey("streamers.id"),
        nullable=False,
    )

    referral_key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("user_id", "bookmaker_id", name="uq_user_bookmaker"),)

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
