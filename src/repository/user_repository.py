from sqlalchemy import select

from ..db.connection import get_db
from ..db.models.users import User


class UserRepository:

    @classmethod
    async def insert_user(cls, name: str, email: str, password: str) -> User:
        async with get_db() as db:
            user = User(name=name, email=email, password=password)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User | None:
        async with get_db() as db:
            return await db.get(User, user_id)
        
    @classmethod
    async def get_user_by_email(cls, email: str) -> User | None:
        async with get_db() as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalars().first()
            return user