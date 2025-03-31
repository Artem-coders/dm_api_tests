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

    # Используем абсолютный путь для CI/CD
    if "CI" in os.environ:  # Проверяем, работает ли в CI
        project_root = Path(os.environ.get("GITHUB_WORKSPACE", "/"))  # Для GitHub Actions, либо пустое значение
        file_path = project_root / "tests" / "swagger-coverage-dm-api-account.html"
    else:
        file_path = current_file_path.parent.parent.parent / "tests" / "swagger-coverage-dm-api-account.html"
    print(f"Ищем файл: {file_path}")

    if not file_path.exists():
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
