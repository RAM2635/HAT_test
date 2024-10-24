import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import aiohttp

# Загружаем переменные окружения из файла .env
load_dotenv()

# Установка токена для бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TUNNEL_URL = os.getenv("TUNNEL_URL")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен. Проверьте файл .env.")
if not TUNNEL_URL:
    raise ValueError("TUNNEL_URL не установлен. Проверьте файл .env.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
try:
    bot = Bot(token=TOKEN)
except Exception as e:
    logging.error(f"Ошибка при создании бота: {e}")
    raise

dp = Dispatcher()

# Создаем маршрутизатор и регистрируем обработчики
router = Router()

@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    tg_id = message.from_user.id

    # Отправляем запрос на сервер для проверки роли пользователя
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{TUNNEL_URL}/sign_in", json={"tg_id": tg_id}) as response:
                if response.status != 200:
                    error_message = await response.text()
                    await message.answer(f"Ошибка входа: {error_message}. Пожалуйста, попробуйте позже.")
                    return

                data = await response.json()
                role = data.get("role")

                if role == "co_builder":
                    await message.answer(
                        "Hi Co-builder! Перейдите по ссылке для продолжения: https://ram2635.github.io/HAT_test/co_builder.html")
                elif role == "founder":
                    await message.answer(
                        "Hi Founder! Перейдите по ссылке для продолжения: https://ram2635.github.io/HAT_test/founder.html")
                else:
                    await message.answer("Ваша роль не найдена. Пожалуйста, свяжитесь с поддержкой.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            await message.answer(f"Произошла ошибка: {e}")

# Включаем маршрутизатор в диспетчер
dp.include_router(router)

async def main():
    # Настройка и запуск бота
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    # Используем asyncio для запуска
    asyncio.run(main())