import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config_reader import config
from handler import router
from StorageFSM import storage_fsm


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )
    dp = Dispatcher(storage=storage_fsm)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
