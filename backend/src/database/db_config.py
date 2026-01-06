from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, registry
from src.config.config import configs

engine = create_async_engine(configs.DATABASE_URL)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
  async with AsyncSession() as session:
    yield session

table_registry = registry()
class Base(DeclarativeBase, MappedAsDataclass):
  registry = table_registry
