from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ram2635.github.io", "https://hylsmk-31-180-193-247.ru.tuna.am"],  # Разрешаем запросы с указанных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Определение модели данных
class OnboardingData(BaseModel):
    startupName: str
    problemSolving: str

# Обработчик для POST-запроса с данными
@app.post("/submit_data")
async def submit_data(request: Request):
    try:
        # Читаем входящие данные в сыром виде
        data = await request.json()
        print(f"Получены данные: {data}")

        # Преобразуем в модель OnboardingData для валидации
        onboarding_data = OnboardingData(**data)
        print(f"Данные прошли валидацию: {onboarding_data}")

        return {"status": "success", "received": onboarding_data.dict()}
    except Exception as e:
        print(f"Ошибка при валидации данных: {e}")
        return {"status": "error", "message": str(e)}

# Обработчик для GET-запроса на корневом уровне
@app.get("/")
def read_root():
    return {"message": "API для Mini App работает!"}
