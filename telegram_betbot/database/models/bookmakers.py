from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


class Bookmaker(Base):
    """Bookmaker model."""

    __tablename__ = "bookmakers"

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    referrals: Mapped[list["Referral"]] = relationship(  # noqa:F821
        "Referral",
        back_populates="bookmaker",
    )  # noqa
