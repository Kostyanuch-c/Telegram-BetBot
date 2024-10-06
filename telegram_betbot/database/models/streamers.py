from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class Streamer(Base):
    """Streamer model."""

    __tablename__ = "streamers"

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    referrals: Mapped[list["Referral"]] = relationship(  # noqa:F821
        "Referral",
        back_populates="streamer",
    )  # noqa
