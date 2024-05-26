import asyncio
import os

from aiogram import Bot, Dispatcher, types


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.admin_private import admin_private_router
from handlers.user_private import user_private_router
from database.engine import create_db, drop_db, session_maker
from database.dp import DataBaseSession

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(admin_private_router)
dp.include_router(user_private_router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown():
    print('Бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool= session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeDefault())
    await create_db()
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())
