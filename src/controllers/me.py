from ..repository.user_repository import UserRepository

from ..app_types.http import ProtectedHttpRequest
from ..utils.http import ok

class MeController:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, data: ProtectedHttpRequest):
        user_id = int(data.get("user_id"))
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if user:
            return ok(body={"user": user.to_dict()})