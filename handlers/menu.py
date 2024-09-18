from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, DialogManager, StartMode, Window, ShowMode
from aiogram.enums import ContentType
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from config import Config

from states import MainMenuSG


router = Router()


async def toggle_spam(callback: CallbackQuery, button: Button, manager: DialogManager):
    print("Spam toggled")


async def message_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    await dialog_manager.switch_to(MainMenuSG.main, show_mode=StartMode.RESET_STACK)

    if message.photo:
        await message.bot.download(
            file=message.photo[-1].file_id, destination="photo.jpg"
        )
        Config.save_message(message.caption, message.photo[0].file_id)
    else:
        Config.save_message(message.text)


menu_window = Window(
    Const("Главное меню"),
    Start(Const("Редактировать сообщение"), id="edit", state=MainMenuSG.message_edit),
    Button(Const("Включить рассылку"), id="toggle_spam", on_click=toggle_spam),
    state=MainMenuSG.main,
)

edit_window = Window(
    Const("Пришли сообщение для рассылки"),
    MessageInput(
        func=message_handler,
        content_types=ContentType.ANY,
    ),
    state=MainMenuSG.message_edit,
)


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)


dialog = Dialog(menu_window, edit_window)
