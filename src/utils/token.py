from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import configs
from src.database.db_config import get_session
from src.models.user_model import UserModel
from src.utils.exceptions import (CouldNotValidateCredentialsError,
                                  NotAdminError, TokenDecodeError,
                                  TokenExpiredSignatureError)

SECRET_KEY: str = configs.SECRET_KEY
TOKEN_EXPIRE: int = configs.TOKEN_EXPIRE
ALGORITHM: str = configs.ALGORITHM


def create_access_token(data: dict) -> str:
    to_encode: dict[Any, Any] = data.copy()
    expire: datetime = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=TOKEN_EXPIRE)
    to_encode.update({"exp": expire})

    encoded_jwt: str = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", refreshUrl="auth/token/refresh")


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):

    try:
        payload: Any = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise CouldNotValidateCredentialsError()

    except DecodeError:
        raise TokenDecodeError()

    except ExpiredSignatureError:
        raise TokenExpiredSignatureError()

    user: UserModel | None = await session.scalar(select(UserModel).where(UserModel.email == email))
    if not user:
        raise CouldNotValidateCredentialsError()

    return user


async def requires_admin(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise NotAdminError()
    return current_user
