from dataclasses import dataclass
from datetime import date
from typing import Literal

@dataclass
class CalculateGoalsParams:
    height: int
    weight: int
    gender: Literal["male", "female"]
    birth_date: date
    activity_level: int
    goal: Literal["lose", "gain", "mantain"]

ACTIVITY_MULTIPLIERS = {
    1: 1.2,
    2: 1.375,
    3: 1.55,
    4: 1.725,
    5: 1.9,
}

def calc_calories(params: CalculateGoalsParams) -> int:
    age = date.today().year - params.birth_date.year

    # Basal Metabolic Rate
    if params.gender == "male":
        bmr = 88.36 + 13.4 * params.weight + 4.8 * params.height - 5.7 * age
    else:
        bmr = 447.6 + 9.2 * params.weight + 3.1 * params.height - 4.3 * age

    # Total Daily Energy Expenditure
    tdee = bmr * ACTIVITY_MULTIPLIERS[params.activity_level]

    if params.goal == "mantain":
        return round(tdee)
    if params.goal == "gain":
        return round(tdee + 500)
    return round(tdee - 500)

def calculate_goals(params: CalculateGoalsParams) -> dict:
    calories = calc_calories(params)
    protein_grams = round(params.weight * 2)
    fat_grams = round(params.weight * 0.9)
    carbs_grams = round((calories - protein_grams * 4 - fat_grams * 9) / 4)

    return {
        "calories": protein_grams * 4 + fat_grams * 9 + carbs_grams * 4,
        "proteins": protein_grams,
        "carbohydrates": carbs_grams,
        "fats": fat_grams,
    }