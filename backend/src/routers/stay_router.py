from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_config import get_session
from src.schemas.stay_schema import StaySchema, StayInternal, StayList, StayCheckout
from src.services.stay_service import StayService
from src.models.stay_model import StayModel
from src.utils.misc import FilterPage

stay_router = APIRouter(prefix="/stay", tags=["Stays"])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def room_service(session: T_Session) -> StayService:
  return StayService(session)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[StayService, Depends(room_service)]

# CHECK IN
@stay_router.post("/check_in", response_model=StayInternal, status_code=201)
async def check_in(service: T_Service, schema: StaySchema) -> StayModel:
  return await service.check_in(schema)


# CHECK OUT
@stay_router.get("/check_out", response_model=StayCheckout)
async def check_out(service: T_Service, guest_id: int) -> StayModel:
  return await service.check_out(guest_id)


# LIST ALL ACTIVE STAYS
@stay_router.get("/actives", response_model=StayList)
async def active_stays(service: T_Service, filter_page: T_FilterPage)-> dict:
  stays = await service.actives_stays(filter_page.limit, filter_page.offset)
  return {"stays": stays}


# LIST ALL ACTIVE STAYS
@stay_router.get("/list", response_model=StayList)
async def list_stays(service: T_Service, filter_page: T_FilterPage)-> dict:
  stays = await service.list_all(filter_page.limit, filter_page.offset)
  return {"stays": stays}
