from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model import UserModel
from src.repositories.user_repository import UserRepository
from src.utils.exceptions import DuplicateEntityError, NotFoundError
from src.utils.hash import hash_password


class UserService():
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)


    #create new user
    async def create_user(self, schema):
        existing_user = await self.repository.verify_data(schema.email)

        if existing_user:
            if existing_user.email == schema.email:
                raise DuplicateEntityError("email", "email already exists in database")

        new_user = UserModel(
            name=schema.name,
            password=hash_password(schema.password),
            email=schema.email,
            is_admin=schema.is_admin
        )

        return await self.repository.create_user(new_user)


    #read user
    async def list_users(self, limit: int, offset: int):
        users = await self.repository.get_users(limit, offset)

        if not users:
            raise NotFoundError()

        return users


    #update user
    async def update_user(self, schema, user_id: int):
        db_user = await self.repository.get_by_id(user_id)

        if not db_user:
            raise NotFoundError()

        db_user.name = schema.name
        db_user.password = hash_password(schema.password)
        db_user.email = schema.email
        db_user.is_admin = schema.is_admin

        return await self.repository.update_user(db_user)


    #delete user
    async def delete_user(self, user_id: int):
        db_user = await self.repository.get_by_id(user_id)

        if not db_user:
            raise NotFoundError()

        return await self.repository.delete_user(user_id)
