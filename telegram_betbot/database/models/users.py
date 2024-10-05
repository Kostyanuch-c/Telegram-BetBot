# from dataclasses import dataclass
"""User model file."""
import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        sa.BigInteger,
        unique=True,
        nullable=False,
    )
