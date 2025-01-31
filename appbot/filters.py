from aiogram.filters import Filter
from aiogram.types import Message
from appbot.config import ADMINS

class Is_Admin(Filter):
    def __call__(self, message: Message):
        return message.from_user.id in ADMINS