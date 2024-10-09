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


class Referral(Base):
    """Referral model."""

    __tablename__ = "referrals"

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

    user: Mapped["User"] = relationship("User", back_populates="referrals")  # noqa:F821
    bookmaker: Mapped["Bookmaker"] = relationship(  # noqa:F821
        "Bookmaker",
        back_populates="referrals",
    )
    streamer: Mapped["Streamer"] = relationship(  # noqa:F821
        "Streamer",
        back_populates="referrals",
    )
