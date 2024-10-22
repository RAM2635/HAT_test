import os
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Установка токена для бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен. Проверьте файл .env.")

# Создаем объект бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем маршрутизатор и регистрируем обработчики
router = Router()


@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    # Отправка ссылки на Mini App, размещенную на GitHub Pages
    await message.answer(
        "Добро пожаловать! Перейдите по ссылке, чтобы начать онбординг: https://ram2635.github.io/HAT_test/")


# Включаем маршрутизатор в диспетчер
dp.include_router(router)


async def main():
    # Настройка и запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Используем asyncio для запуска
    asyncio.run(main())
