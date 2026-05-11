import pytest

from src.utils.parse_protected_event import parse_protected_event
from src.controllers.get_meal_by_id import GetMealByIdController
from src.repository.meal_repository import MealRepository


@pytest.mark.asyncio
async def test_get_meal_by_id_successfully(test_session_db, test_login_user, test_meal):
    meal_repository = MealRepository(db_session=test_session_db)
    get_meal_controller = GetMealByIdController(meal_repository)

    event = {
        "headers": {"authorization": f"Bearer {test_login_user}"},
        "pathParameters": {
            "meal_id": str(test_meal.id)
        }
    }

    request = parse_protected_event(event=event)
    response = await get_meal_controller.handle(request)
    assert response["body"]["meal"] == test_meal.to_dict