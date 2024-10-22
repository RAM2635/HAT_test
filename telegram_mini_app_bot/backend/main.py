from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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

@app.post("/submit_data")
async def submit_data(data: dict):
    # Логика обработки данных стартапа
    print(f"Получены данные: {data}")
    return {"message": "Данные успешно получены", "data": data}
