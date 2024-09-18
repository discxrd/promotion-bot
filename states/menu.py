from aiogram.filters.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    main = State()
    message_edit = State()
