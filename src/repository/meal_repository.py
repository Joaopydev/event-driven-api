from datetime import date, datetime
from typing import List, Dict
from sqlalchemy import select, update

from ..db.connection import get_db
from ..db.models.meals import InputType, MealStatus, Meal


class MealRepository:

    @classmethod
    async def create_meal(
        cls,
        user_id: int,
        input_file_key: str,
        file_type: str
    ) -> Meal:
        
        async with get_db() as db:
            meal = Meal(
                user_id=user_id,
                status=MealStatus.uploading,
                input_file_key=input_file_key,
                input_type=InputType.audio if file_type == "audio/m4a" else InputType.picture,
                icon="",
                name="",
                foods=[],
            )

            db.add(meal)
            await db.commit()
            await db.refresh(meal)

            return meal
        
    
    @classmethod
    async def get_meal_by_id(cls, meal_id: str, user_id: int) -> Meal | None:
        async with get_db() as db:
            query = select(Meal).where(
                Meal.id == meal_id,
                Meal.user_id == user_id
            )
            result = await db.execute(query)
            return result.scalars().first()
        
    
    @classmethod
    async def get_meal_by_file_key(cls, file_key: str) -> Meal | None:
        async with get_db() as db:
            query = select(Meal).where(Meal.input_file_key == file_key)
            result = await db.execute(query)
            return result.scalars().first()
        
    
    @classmethod
    async def list_meals_by_date(cls, user_id: int, start_date: date, end_date: datetime) -> List[Meal]:
        async with get_db() as db:
            query = select(Meal).where(
                Meal.user_id == user_id,
                Meal.status == MealStatus.success,
                Meal.created_at >= start_date,
                Meal.created_at <= end_date,
            )
            result = await db.execute(query)
            meals = result.scalars().all()
            return meals
        

    @classmethod
    async def update_meal_status(cls, meal_id: str, new_status: MealStatus) -> None:
        async with get_db() as db:
            await db.execute(
                update(Meal)
                .where(Meal.id == meal_id)
                .values(status=new_status)
            )
            await db.commit()

    
    @classmethod
    async def update_meal_data(
        cls,
        meal_id: str,
        new_status: MealStatus,
        name: str,
        icon: str,
        foods: List[Dict[str, any]]
    ):
        async with get_db() as db:
            await db.execute(
                update(Meal)
                .where(Meal.id == meal_id)
                .values(
                    status=new_status,
                    name=name,
                    icon=icon,
                    foods=foods,
                )
            )
            await db.commit()