from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.user_model import UserModel
from src.utils.exceptions import CouldNotValidateCredentialsError
from src.utils.hash import verify_password
from src.utils.token import create_access_token, get_current_user

auth_router = APIRouter()

OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[UserModel, Depends(get_current_user)]


# ========= LOGIN ROUTER =========
@auth_router.post("/login")
async def login_token(session: T_Session, form_data: OAuth2):
    user = await session.scalar(select(UserModel).where(UserModel.email == form_data.username))

    if not user:
        raise CouldNotValidateCredentialsError()

    if not verify_password(form_data.password, user.password):
        raise CouldNotValidateCredentialsError()

    access_token = create_access_token({"sub": user.email, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "Bearer"}


# ========= REFRESH TOKEN ROUTER =========
@auth_router.post("/refresh_token")
async def refresh_token(user: T_CurrentUser):
    new_token = create_access_token({"sub": user.email, "is_admin": user.is_admin})
    return {"access_token": new_token, "token_type": "Bearer"}
