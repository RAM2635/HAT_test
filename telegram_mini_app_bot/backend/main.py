import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Table, MetaData
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

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
    Column("startup", String)
)

# Модель для данных пользователя
class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: str

@app.post("/register")
async def register_user(user: User):
    async with async_session() as session:
        async with session.begin():
            existing_user = await session.execute(users_table.select().where(users_table.c.email == user.email))
            if existing_user.scalar():
                raise HTTPException(status_code=400, detail="User with this email is already registered")

            new_user = users_table.insert().values(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role
            )
            await session.execute(new_user)
            await session.commit()

    return {"message": "Registration successful", "user": user.first_name}