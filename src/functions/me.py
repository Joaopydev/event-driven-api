import asyncio
from typing import Dict, Any


from ..utils.parse_protected_event import parse_protected_event
from ..utils.parse_response import parse_response
from ..utils.http import unauthorized
from ..app_types.http import HTTPResponse
from ..controllers.me import MeController
from ..exceptions.AccessTokenNotProvided import AccessTokenNotProvided
from ..exceptions.InvalidAccessToken import InvalidAccessToken
from ..repository.user_repository import UserRepository


async def async_handler(event: Dict[str, Any], context: Any) -> HTTPResponse:
    response = None
    try:
        request = parse_protected_event(event=event)
        controller = MeController(UserRepository())
        response = await controller.handle(data=request)
    except AccessTokenNotProvided:
        response = unauthorized(body={"error": "Access token not provided."})
    except InvalidAccessToken:
        response = unauthorized(body={"error": "Invalid access token"})
    finally:
        return parse_response(response=response)
    

def handler(event: Dict[str, Any], context: Any) -> HTTPResponse:
    return asyncio.run(async_handler(event=event, context=context))