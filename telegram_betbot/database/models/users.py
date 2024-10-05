# from dataclasses import dataclass
"""User model file."""
from sqlalchemy import (
    BigInteger,
    Enum,
    Float,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from telegram_betbot.tgbot.enums.role import Role

from .base import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )
    """User model."""

    """ Telegram user id """
    user_name: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )
    """ Telegram user name """
    first_name: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )
    """ Telegram profile first name """
    last_name: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )
    """ Telegram profile second name """
    language_code: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )
    """ Telegram profile language code """

    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    """ User's role """

    # status: Mapped[Status] = mapped_column(Enum(Role), default=Status....
    # """ User's status """

    time_difference_moscow: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    """User's time difference moscow '"""
