from sqlalchemy.ext.asyncio import AsyncSession
from src.models.room_model import RoomStatus
from src.models.stay_model import StayModel, StayStatus
from src.repositories.room_repository import RoomRepository
from src.repositories.stay_repository import StayRepository
from src.utils.exceptions import (
    DuplicateEntityError,
    RoomNotAvaliableError,
    StayNotFoundError,
)


class StayService:
    def __init__(self, session: AsyncSession) -> None:
        self.stay_repo = StayRepository(session)
        self.room_repo = RoomRepository(session)

    # CHECK IN
    async def check_in(self, schema):
        existing_stay = await self.stay_repo.get_active_stay_by_guest_id(
            schema.guest_id
        )

        if existing_stay:
            raise DuplicateEntityError("stay", "stay already exists")

        room = await self.room_repo.get_by_id(schema.room_number)
        if room is None:
            raise StayNotFoundError()

        if room.status != RoomStatus.AVAILABLE:
            raise RoomNotAvaliableError()

        new_stay = StayModel(
            room_number=schema.room_number,
            guest_id=schema.guest_id,
            check_in_date=schema.check_in_date,
            check_out_date=schema.check_out_date,
            status=StayStatus.ACTIVE,
        )
        room.status = RoomStatus.OCCUPIED
        await self.room_repo.update_room(room)

        return await self.stay_repo.create_stay(new_stay)

    # CHECK OUT
    async def check_out(self, guest_id: int):
        stay = await self.stay_repo.get_active_stay_by_guest_id(guest_id)
        if stay is None:
            raise StayNotFoundError()

        room = await self.room_repo.get_by_id(stay.room_number)
        if room is None:
            raise StayNotFoundError()

        room.status = RoomStatus.AVAILABLE
        stay.status = StayStatus.FINISHED
        # stay.check_out_date = datetime.now()

        diff = stay.check_out_date - stay.check_in_date
        days = max(1, diff.days)
        stay.total_price = days * room.daily_price  # type: ignore

        await self.room_repo.update_room(room)
        return await self.stay_repo.update_stay(stay)

    # LIST ALL STAYS
    async def list_all(self, limit: int, offset: int):
        stays = await self.stay_repo.list_stays(limit, offset)

        if stays is None:
            raise StayNotFoundError()

        return stays

    # LIST ALL ACTIVES STAYS
    async def actives_stays(self, limit: int, offset: int):
        stays = await self.stay_repo.active_stays(limit, offset)

        if stays is None:
            raise StayNotFoundError()

        return stays
