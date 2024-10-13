"""Repository file."""
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_betbot.database.models import Base


AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    """Repository abstract class."""

    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        """Get an ONE model from the database with PK."""
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause, options: list | None = None) -> AbstractModel | None:
        """Get an ONE model from the database with whereclause.

        :param whereclause: Clause by which entry will be found
        :param options: Which options will be used for operations
        :return: Model if only one model was found, else None.
        """
        statement = select(self.type_model).where(whereclause)
        if options:
            statement = statement.options(*options)

        return (await self.session.execute(statement)).scalar_one_or_none()

    async def get_many(
        self,
        whereclause,
        order_by=None,
        options: list | None = None,
    ) -> Sequence:
        """Get many models from the database with whereclause."""
        statement = select(self.type_model).where(whereclause)
        if order_by:
            statement = statement.order_by(order_by)
        if options:
            statement = statement.options(*options)

        return (await self.session.scalars(statement)).all()

    async def delete(self, whereclause) -> None:
        """Delete model from the database.

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)
