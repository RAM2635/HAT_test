import os
import traceback
import logging

from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Table, MetaData, select
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Загрузка переменных окружения из .env файла
load_dotenv()

# Подключение к базе данных через SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не установлен. Проверьте файл .env.")

TUNNEL_URL = os.getenv("TUNNEL_URL")
if not TUNNEL_URL:
    raise ValueError("TUNNEL_URL не установлен. Проверьте файл .env.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажите здесь список доменов, которым разрешён доступ
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="telegram_mini_app_bot/app"), name="static")

templates = Jinja2Templates(directory="templates")

metadata = MetaData()

# Таблица пользователей
users_table = Table(
    "users",
    metadata,
    Column("tg_id", BigInteger, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String, unique=True),
    Column("id", Integer),
    Column("role", String),
    Column("startup", String),
    schema="public"
)


# Модель данных для регистрации пользователя
class User(BaseModel):
    tg_id: int
    email: EmailStr  # Используем EmailStr для валидации email адреса
    first_name: str
    last_name: str
    role: str


# Модель данных для входа по tg_id
class SignInData(BaseModel):
    tg_id: int


# Функция для отправки сообщений через Telegram API с учетом длины сообщения
async def send_message(chat_id: int, message: str):
    MAX_LENGTH = 4096

    if len(message) > MAX_LENGTH:
        for i in range(0, len(message), MAX_LENGTH):
            part = message[i:i + MAX_LENGTH]
            # Здесь добавьте логику для отправки каждой части сообщения через Telegram API.
            logging.info(f"Sending part of the message to {chat_id}: {part}")
            # await bot.send_message(chat_id=chat_id, text=part)  # Реальная логика отправки сообщения
    else:
        logging.info(f"Sending message to {chat_id}: {message}")
        # await bot.send_message(chat_id=chat_id, text=message)  # Реальная логика отправки сообщения


# Эндпоинт для регистрации нового пользователя
@app.post("/register")
async def register_user(user: User):
    async with async_session() as session:
        async with session.begin():
            existing_user_by_tg_id = await session.execute(select(users_table).where(users_table.c.tg_id == user.tg_id))
            if existing_user_by_tg_id.scalar():
                raise HTTPException(status_code=400, detail="User with this tg_id is already registered")

            existing_user_by_email = await session.execute(select(users_table).where(users_table.c.email == user.email))
            if existing_user_by_email.scalar():
                raise HTTPException(status_code=400, detail="User with this email is already registered")

            new_user = users_table.insert().values(
                tg_id=user.tg_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role
            )
            await session.execute(new_user)
            await session.commit()

    return {"message": "Registration successful", "user": user.first_name}


# Эндпоинт для входа пользователя по tg_id
@app.post("/sign_in")
async def sign_in_user(sign_in_data: SignInData):
    logging.info(f"Received sign_in request with tg_id: {sign_in_data.tg_id}")

    try:
        async with async_session() as session:
            async with session.begin():
                query = select(users_table).where(users_table.c.tg_id == sign_in_data.tg_id)
                result = await session.execute(query)
                user = result.fetchone()

                if not user:
                    logging.warning("User not found")
                    raise HTTPException(status_code=404, detail="User not found")

                logging.info(f"User found: tg_id={user.tg_id}, role={user.role}")

                await send_message(user.tg_id, "Welcome back!")  # Пример использования функции send_message

                return {"tg_id": user.tg_id, "role": user.role}
    except Exception as e:
        logging.error(f"An error occurred during sign in: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


# Остальные маршруты остаются без изменений...

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "TUNNEL_URL": TUNNEL_URL})


@app.get("/registration")
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request, "TUNNEL_URL": TUNNEL_URL})


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "TUNNEL_URL": TUNNEL_URL})


@app.get("/co_builder")
async def co_builder(request: Request):
    return templates.TemplateResponse("co_builder.html", {"request": request})


@app.get("/founder")
async def founder(request: Request):
    return templates.TemplateResponse("founder.html", {"request": request})


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP exception occurred: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )