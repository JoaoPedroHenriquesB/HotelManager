from sqlalchemy.ext.asyncio import AsyncSession
from src.models.guest_model import GuestModel
from src.repositories.guest_repository import GuestRepository
from src.utils.exceptions import DuplicateEntityError, NotFoundError


class GuestService:
  def __init__(self, session: AsyncSession) -> None:
    self.repository = GuestRepository(session)


  # CREATE NEW GUEST
  async def create_guest(self, schema):
    existing_guest = await self.repository.verify_data(schema.cpf)

    if existing_guest:
      if existing_guest.cpf == schema.cpf:
        raise DuplicateEntityError("cpf", "cpf already exists in database")

    new_guest = GuestModel(
      name=schema.name,
      phone_number=schema.phone_number,
      cpf=schema.cpf,
      room_number=schema.room_number
    )

    return await self.repository.create_guest(new_guest)


  # LIST ALL GUESTS
  async def list_guests(self, limit:int, offset:int):
    guests = await self.repository.get_guests(limit, offset)

    if not guests:
      raise NotFoundError()

    return guests


  # UPDATE GUEST
  async def update_guest(self, schema, guest_id):
    db_guest = await self.repository.get_by_id(guest_id)

    if not db_guest:
      raise NotFoundError()

    db_guest.name = schema.name
    db_guest.phone_number = schema.phone_number
    db_guest.cpf = schema.cpf
    db_guest.room_number = schema.room_number

    return await self.repository.update_guest(db_guest)


  # DELETE GUEST
  async def delete_guest(self, guest_id):
    db_guest = await self.repository.get_by_id(guest_id)

    if not db_guest:
      raise NotFoundError()

    return await self.repository.delete_guest(guest_id)
