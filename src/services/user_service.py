from typing import Any, Dict, Sequence

from src.models.user_model import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserSchema
from src.utils.exceptions import DuplicateEntityError, NotFoundError
from src.utils.hash import hash_password


class UserService():
    def __init__(self, repository: UserRepository) -> None:
        self.repository: UserRepository = repository


    # --- CREATE ---
    async def create(self, schema: UserSchema) -> UserModel:
        """
        encrypts the password and persists a new user in the database.
        checks if the email is already registered before creating the new user.
        hashes the password using the security utility function.

        args:
            schema: Object containing the creation data (email, password, etc.).

        returns:
            UserModel: The newly created user object with ID and timestamp.

        raises:
            DuplicateEntityError: If the provided email already exists in the system.
        """
        existing_user: UserModel | None = await self.repository.get_by_email(email=schema.email)
        if existing_user:
            raise DuplicateEntityError(field="email", message="email already exists in database")

        user_data: Dict[str, Any] = schema.model_dump()
        user_data["password"] = hash_password(password=user_data["password"])

        new_user = UserModel(**user_data)
        return await self.repository.create_user(user_model=new_user)


    # --- READ ---
    async def list(self, limit: int, offset: int) -> Sequence[UserModel]:
        """
        retrieves a list of users with pagination.

        args:
            limit: Maximum number of users to return.
            offset: Number of users to skip before starting to collect the result set.

        returns:
            Sequence[UserModel]: A list of user objects.
        """
        users: Sequence[UserModel] = await self.repository.list(limit=limit, offset=offset)
        return users


    # --- UPDATE ---
    async def update(self, schema: UserSchema, user_id: int) -> UserModel:
        """
        updates an existing user's information.
        only the fields provided in the schema (set fields) will be updated.
        if a new password is provided, it will be automatically hashed.

        args:
            schema: Object containing the fields to be updated.
            user_id: Unique identifier of the user to update.

        returns:
            UserModel: The updated user object.

        raises:
            NotFoundError: If no user is found with the provided ID.
        """
        db_user: UserModel | None = await self.repository.get_by_id(user_id=user_id)
        if not db_user:
            raise NotFoundError()

        update_data: Dict[str, Any] = schema.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = hash_password(password=update_data["password"])

        for key, value in update_data.items():
            setattr(db_user, key, value)

        return await self.repository.update_user(user_model=db_user)


    # --- DELETE ---
    async def delete(self, user_id: int) -> None:
        """
        Deletes a user from the database.

        Args:
            user_id: ID of the user to be deleted.

        Raises:
            NotFoundError: If the user does not exist.
        """
        db_user: UserModel | None = await self.repository.get_by_id(user_id=user_id)
        if not db_user:
            raise NotFoundError()

        await self.repository.delete_user(user_model=db_user)
