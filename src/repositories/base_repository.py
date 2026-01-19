from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def _commit_or_rollback(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
