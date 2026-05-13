from enum import Enum
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, LargeBinary, Enum as SQLEnum, Date

from .base import Base

class GoalType(Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"

class GenderType(Enum):
    female = "female"
    male = "male"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    goal: Mapped[GoalType] = mapped_column(SQLEnum(GoalType), nullable=False)
    gender: Mapped[GenderType] = mapped_column(SQLEnum(GenderType), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_level: Mapped[int] = mapped_column(Integer, nullable=False)

    #Goals
    calories: Mapped[int] = mapped_column(Integer, nullable=False)
    proteins: Mapped[int] = mapped_column(Integer, nullable=False)
    carbohydrates: Mapped[int] = mapped_column(Integer, nullable=False)
    fats: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "calories": self.calories,
            "proteins": self.proteins,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
        }
        