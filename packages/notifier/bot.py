import os
from pathlib import Path
from telebot import TeleBot
from vyper import v

# Получаем абсолютный путь до текущего файла
current_file_path = Path(__file__).resolve()

# Настройка конфигурации
config = current_file_path.parent.joinpath("../../").joinpath("config")
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()


def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))

    # Строим путь к файлу относительно корня проекта
    file_path = current_file_path.parent.parent / "tests" / "swagger-coverage-dm-api-account.html"

    # Логируем путь к файлу
    print(f"Ищем файл: {file_path}")

    # Проверка, существует ли файл
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден по пути: {file_path}")

    # Логируем успешное нахождение файла
    print(f"Файл найден: {file_path}")

    # Открываем и отправляем файл
    with open(file_path, "rb") as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption="coverage",
        )


if __name__ == '__main__':
    send_file()
