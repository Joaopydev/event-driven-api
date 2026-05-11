from sqlalchemy import select

from ..db.connection import get_db
from ..db.models.users import User


class UserRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    async def insert_user(self, name: str, email: str, password: str) -> User:
        async with self.db_session() as db:
            user = User(name=name, email=email, password=password)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        async with self.db_session() as db:
            return await db.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.db_session() as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalars().first()
            return user