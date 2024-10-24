# backend/main.py

import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Table, MetaData
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Подключение к базе данных через SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не установлен. Проверьте файл .env.")

TUNNEL_URL = os.getenv("TUNNEL_URL")
if not TUNNEL_URL:
    raise ValueError("TUNNEL_URL не установлен. Проверьте файл .env.")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

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
    email: str
    first_name: str
    last_name: str
    role: str

# Модель данных для входа по tg_id
class SignInData(BaseModel):
    tg_id: int

# Эндпоинт для регистрации нового пользователя
@app.post("/register")
async def register_user(user: User):
    async with async_session() as session:
        async with session.begin():
            # Проверка, зарегистрирован ли пользователь по tg_id
            existing_user = await session.execute(users_table.select().where(users_table.c.tg_id == user.tg_id))
            if existing_user.scalar():
                raise HTTPException(status_code=400, detail="User with this tg_id is already registered")

            # Вставка нового пользователя
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
    print(f"Received sign_in request with tg_id: {sign_in_data.tg_id}")
    try:
        async with async_session() as session:
            async with session.begin():
                # Проверка пользователя по tg_id
                query = users_table.select().where(users_table.c.tg_id == sign_in_data.tg_id)
                result = await session.execute(query)
                user = result.fetchone()

                if not user:
                    print("User not found")
                    raise HTTPException(status_code=404, detail="User not found")

                print(f"User found: tg_id={user.tg_id}, role={user.role}")
                return {"tg_id": user.tg_id, "role": user.role}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Маршруты для HTML-страниц
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

