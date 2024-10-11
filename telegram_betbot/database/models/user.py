"""User model file."""
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Enum,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from telegram_betbot.tgbot.enums.role import Role

from .base import Base


if TYPE_CHECKING:
    from .referral import Referral


class User(Base):
    """User model."""

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

    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    chat_type: Mapped[str] = mapped_column(String, nullable=False, unique=False)

    referrals: Mapped[list["Referral"]] = relationship(
        "Referral",
        back_populates="user",
    )
    """User referrals """
