import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from src.config.config import configs
from src.database.db_config import table_registry

from src.models.room_model import RoomModel  # noqa: F401
from src.models.stay_model import StayModel  # noqa: F401
from src.models.guest_model import GuestModel  # noqa: F401
from src.models.user_model import UserModel # noqa: F401

config = context.config

config.set_main_option("sqlalchemy.url", configs.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = table_registry.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():

    database_url = config.get_main_option("sqlalchemy.url")

    if database_url is None:
        raise ValueError("A URL do banco de dados não foi encontrada na configuração do Alembic.")

    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
