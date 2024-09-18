import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import setup_dialogs

from pyrogram import Client
from pyrogram.enums import ChatType

from handlers import menu_router, menu_dialog

from config import Config


async def spam_thread() -> None:
    async with Client("account", api_id=Config.API_ID, api_hash=Config.API_HASH) as app:
        while True:
            try:
                data = Config.load_message()
            except Exception as e:
                asyncio.sleep(10)
                continue

            message = data["m"]
            photo_id = data["p"]

            async for dialog in app.get_dialogs():
                if (
                    dialog.chat.type == ChatType.SUPERGROUP
                    or dialog.chat.type == ChatType.GROUP
                ):
                    if "NitroCode" not in dialog.chat.title:
                        try:
                            if photo_id:
                                await app.send_photo(
                                    dialog.chat.id,
                                    photo="photo.jpg",
                                    caption=message,
                                )
                            else:
                                await app.send_message(dialog.chat.id, text=message)
                        except Exception as e:
                            if "USER_BANNED" in str(e):
                                await asyncio.sleep(200)
                            print(e, dialog.chat.title)

                    await asyncio.sleep(5)

            await asyncio.sleep(35)


async def main() -> None:
    storage = MemoryStorage()
    bot = Bot(token=Config.TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_routers(menu_dialog)
    dp.include_routers(menu_router)

    setup_dialogs(dp)

    await spam_thread()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
