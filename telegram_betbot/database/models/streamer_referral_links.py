from sqlalchemy import (
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


class StreamerReferralLink(Base):
    """StreamerReferralLink model."""

    __tablename__ = "streamer_referral_links"

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
    bookmaker = relationship("Bookmaker", back_populates="referral_links")
    streamer = relationship("Streamer", back_populates="referral_links")
