from datetime import date
from sqlalchemy import select

from ..db.models.users import User, GoalType, GenderType


class UserRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    async def insert_user(
        self,
        name: str,
        email: str,
        password: str,
        goal: GoalType,
        gender: GenderType,
        birth_date: date,
        height: int,
        weight: int,
        activity_level: int,
        calories: int,
        proteins: int,
        carbohydrates: int,
        fats: int

    ) -> User:
        async with self.db_session() as db:
            user = User(
                name=name,
                email=email,
                password=password,
                goal=goal,
                gender=gender,
                birth_date=birth_date,
                height=height,
                weight=weight,
                activity_level=activity_level,
                calories=calories,
                proteins=proteins,
                carbohydrates=carbohydrates,
                fats=fats,
            )
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