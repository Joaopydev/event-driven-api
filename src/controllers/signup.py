from typing import Dict, AnyStr, Optional
from pydantic import BaseModel, ValidationError, EmailStr

from ..lib.jwt import signin_access_token
from ..app_types.http import HTTPResponse
from ..utils.http import created, bad_request, conflict

from ..repository.user_repository import UserRepository
from ..services.hashed_service import HashedPasswordService


class EventSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignupController:

    def __init__(self, user_repository: UserRepository, hashed_service: HashedPasswordService):
        self.user_repository = user_repository
        self.hashed_service = hashed_service

    def _validate_body(self, body: Dict[str, AnyStr]) -> EventSchema:
        return EventSchema(**body)
    
    async def handle(self, body: Dict[str, AnyStr]) -> HTTPResponse:
        try:
            data = self._validate_body(body)
        except ValidationError as ex:
            return bad_request(body={"errors": ex.errors()})
        
        body = data.model_dump()
        user = await self.user_repository.get_user_by_email(email=body["email"])
        if user:
            return conflict(body={"error": "Email already exists"})
            
        hashed_password = self.hashed_service.hash_password(password=body.get("password"))
        new_user = await self.user_repository.insert_user(
            name=body.get("name"),
            email=body.get("email"),
            password=hashed_password
        )
        access_token = signin_access_token(user_id=new_user.id)
        return created(body={"access_token": access_token})