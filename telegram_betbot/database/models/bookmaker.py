from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


if TYPE_CHECKING:
    from .referral import Referral
    from .streamer import Streamer


class Bookmaker(Base):
    """Bookmaker model."""

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    referrals: Mapped[list["Referral"]] = relationship(
        "Referral",
        back_populates="bookmaker",
    )

    streamers: Mapped[list["Streamer"]] = relationship(
        back_populates="bookmakers",
        secondary="streamer_bookmaker_memberships",
    )
