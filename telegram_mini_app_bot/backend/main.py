from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API для Mini App работает!"}

@app.post("/submit_data")
def submit_data(data: dict):
    # Логика обработки данных из Mini App
    return {"status": "success", "data_received": data}
