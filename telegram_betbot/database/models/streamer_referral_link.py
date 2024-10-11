from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class StreamerBookmakerMembership(Base):
    """StreamerBookmakerMembership model."""

    __tablename__ = "streamer_bookmaker_memberships"
    streamer_id: Mapped[int] = mapped_column(
        ForeignKey("streamers.id"),
        primary_key=True,
    )
    bookmaker_id: Mapped[int] = mapped_column(
        ForeignKey("bookmakers.id"),
        primary_key=True,
    )
    referral_link: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("streamer_id", "bookmaker_id", name="uq_streamer_bookmaker"),
    )
