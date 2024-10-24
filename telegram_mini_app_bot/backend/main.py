import os
from fastapi import FastAPI, HTTPException, Depends
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

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

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
    schema="public"  # Указание схемы public
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
    async with async_session() as session:
        async with session.begin():
            # Проверка пользователя по tg_id
            query = users_table.select().where(users_table.c.tg_id == sign_in_data.tg_id)
            result = await session.execute(query)
            user = result.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {"tg_id": user.tg_id, "role": user.role}
