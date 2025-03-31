import os
from pathlib import Path
from telebot import TeleBot
from vyper import v

current_file_path = Path(__file__).resolve()

config = current_file_path.parent.joinpath("../../").joinpath("config")
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()

def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))

    file_path = os.path.join(current_file_path.parent.parent.parent, "swagger-coverage-dm-api-account.html")
    print(f"Ищем файл: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден по пути: {file_path}")

    print(f"Файл найден: {file_path}")
    with open(file_path, "rb") as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption="coverage",
        )

if __name__ == '__main__':
    send_file()
