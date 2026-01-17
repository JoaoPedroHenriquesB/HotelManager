from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.user_model import UserModel

T_Session = Annotated[AsyncSession, Depends(get_session)]

class UserRepository:
    def __init__(self, session: T_Session) -> None:
        self.session = session

    #verify email
    async def verify_data(self, email: str):
        return await self.session.scalar(select(UserModel).where((UserModel.email == email)))


    #get by id
    async def get_by_id(self, user_id: int):
        return await self.session.scalar(select(UserModel).where(UserModel.id == user_id))


    #create new user
    async def create_user(self, user_model: UserModel):
        try:
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            return user_model

        except SQLAlchemyError:
            await self.session.rollback()
            raise


    #read user
    async def get_users(self, limit: int, offset: int):
        result = await self.session.scalars(select(UserModel).limit(limit).offset(offset))
        return result.all()


    #update user
    async def update_user(self, user_model: UserModel):
        try:
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
            return user_model

        except SQLAlchemyError:
            await self.session.rollback()
            raise


    #delete user
    async def delete_user(self, user_id):
        try:
            user_to_delete = await self.session.get(UserModel, user_id)
            await self.session.delete(user_to_delete)
            await self.session.commit()

        except SQLAlchemyError:
            await self.session.rollback()
            raise
