from typing import Annotated, Sequence, Tuple

from fastapi import Depends
from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.user_model import UserModel
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    # --- READ ---
    async def get_by_id(self, user_id: int) -> UserModel | None:
        return await self.session.get(entity=UserModel, ident=user_id)


    async def get_by_email(self, email: str) -> UserModel | None:
        stmt: Select[Tuple[UserModel]] = select(UserModel).where(UserModel.email == email)
        return await self.session.scalar(statement=stmt)


    async def list(self, limit: int, offset: int) -> Sequence[UserModel]:
        result: ScalarResult[UserModel] = await self.session.scalars(statement=select(UserModel).limit(limit=limit).offset(offset=offset))
        return result.all()


    # --- WRITE ---
    async def create_user(self, user_model: UserModel) -> UserModel:
        """Persists a new user record in the database."""
        self.session.add(instance=user_model)
        await self._commit_or_rollback()
        await self.session.refresh(instance=user_model)
        return user_model


    async def update_user(self, user_model: UserModel) -> UserModel:
        """Commits changes to an existing user record."""
        self.session.add(instance=user_model)
        await self._commit_or_rollback()
        await self.session.refresh(instance=user_model)
        return user_model


    async def delete_user(self, user_model: UserModel) -> None:
        """
        Removes a user record from the database.

        Args:
            user_id: The ID of the user to be deleted.

        Raises:
            SQLAlchemyError: If the deletion fails.
        """
        await self.session.delete(instance=user_model)
        await self._commit_or_rollback()
