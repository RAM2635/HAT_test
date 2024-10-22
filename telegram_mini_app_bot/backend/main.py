import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

app = FastAPI()

# Получение URL туннеля из .env файла
TUNNEL_URL = os.getenv("TUNNEL_URL")

# Модель для данных пользователя
class User(BaseModel):
    username: str
    email: str
    password: str

# Словарь для хранения пользователей (вместо базы данных)
users_db = {}

@app.post("/register")
async def register_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    # Сохраняем пользователя в "базе данных"
    users_db[user.email] = {
        "username": user.username,
        "password": user.password  # Не рекомендуется хранить пароли в открытом виде!
    }
    return {"message": "Регистрация успешна", "user": user.username}

@app.get("/get_tunnel_url")
async def get_tunnel_url():
    return {"tunnel_url": TUNNEL_URL}
