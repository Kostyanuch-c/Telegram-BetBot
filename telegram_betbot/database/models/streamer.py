from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


if TYPE_CHECKING:
    from .bookmaker import Bookmaker
    from .referral import Referral


class Streamer(Base):
    """Streamer model."""

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    referrals: Mapped[list["Referral"]] = relationship(
        "Referral",
        back_populates="streamer",
    )

    bookmakers: Mapped[list["Bookmaker"]] = relationship(
        back_populates="streamers",
        secondary="streamer_bookmaker_memberships",
    )
