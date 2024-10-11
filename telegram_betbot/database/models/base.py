"""Base model."""
from sqlalchemy import BigInteger, MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
)


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


@as_declarative(metadata=metadata)
class Base:
    """Abstract model with declarative base functionality."""

    __abstract__ = True
    __allow_unmapped__ = False

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(  # noqa:A003
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
