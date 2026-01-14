from sqlalchemy.orm import Mapped, mapped_column

from src.database.db_config import Base


class GuestModel(Base):
  __tablename__ = "guests"

  id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
  name: Mapped[str]
  phone_number: Mapped[str]
  cpf: Mapped[str]
