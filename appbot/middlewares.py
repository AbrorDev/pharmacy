import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject

from appbot.config import ADMINS, OWNERS

logger = logging.getLogger(__name__)


class AuthorizationMiddleware(BaseMiddleware):
    """
    Helps to check if user is authorized to use the bot
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        authorization = get_flag(data, "authorization")
        # print("Authorization: ", authorization)
        if authorization is not None:
            if authorization["is_authorized"]:
                if event.chat.id in ADMINS:
                    return await handler(event, data)
                else:
                    return None
        else:
            return await handler(event, data)

class OwnerAuthorizationMiddleware(BaseMiddleware):
    """
    Helps to check if user is authorized to use the bot
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        owner_authorization = get_flag(data, "owner_authorization")
        if owner_authorization is not None:
            if owner_authorization["is_owner_authorized"]:
                if event.chat.id in OWNERS:
                    return await handler(event, data)
                else:
                    return None
        else:
            return await handler(event, data)