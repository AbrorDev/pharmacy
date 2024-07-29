import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from appbot.handlers import router
from appbot.admins import router_admin
from appbot.owners import router_owner
from appbot.middlewares import AuthorizationMiddleware, OwnerAuthorizationMiddleware
from appbot.config import ADMINS

bot = Bot(token='7097819289:AAEqPHg-e3ndVApWrxA_BAeZREUuKhjB8xQ')
dp = Dispatcher()

async def startup_answer(bot: Bot):
    for admin in ADMINS:
        await bot.send_message(admin, "Bot ishga tushdi✅")


async def shutdown_answer(bot: Bot):
    for admin in ADMINS:
        await bot.send_message(admin, "Bot ishlashdan to'xtadi❌")



async def main():
    dp.startup.register(startup_answer)
    dp.include_routers(router_owner, router_admin, router)
    dp.message.middleware(AuthorizationMiddleware())
    dp.message.middleware(OwnerAuthorizationMiddleware())
    dp.shutdown.register(shutdown_answer)

    await bot.set_my_commands([
        types.BotCommand(command='/start', description='Botni ishga tushirish'),
        types.BotCommand(command='/help', description='Yordam olish')
    ])
    await dp.start_polling(bot)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')