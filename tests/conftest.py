import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.db.models.base import Base
from src.services.hashed_service import HashedPasswordService
from src.repository.user_repository import UserRepository

@pytest.fixture
async def test_engine():
    engine = create_async_engine(
        url="sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
  
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session_db(test_engine):
    async_session = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.fixture
async def test_user(test_session_db):
    password_hash = HashedPasswordService.hash_password("password")
    user_repository = UserRepository(db_session=lambda: test_session_db)
    user = await user_repository.insert_user(
        name="Teste",
        email="test@gmail.com",
        password=password_hash,
    )
    return user