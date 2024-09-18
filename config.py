import json


class Config:
    # bot
    TOKEN = ""

    # account
    API_ID = 
    API_HASH = ""

    # others
    ADMINS_IDS = []

    def save_message(
        message: str,
        photo_id: str = None,
    ):
        with open("message.txt", "w") as file:
            data = {"m": message, "p": photo_id}
            json.dump(data, file)

    def load_message():
        with open("message.txt", "r") as file:
            data = json.load(file)

            return data
