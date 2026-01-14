from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db_config import Base


class UserModel(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
  name: Mapped[str]
  password: Mapped[str]
  email: Mapped[str] = mapped_column(unique=True)
  is_admin: Mapped[bool] = mapped_column(default=False, init=True, server_default=text('false'))
