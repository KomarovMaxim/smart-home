
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from . import crud
from .models import Device, ToggleResponse
from .database import Base, engine, SessionLocal, get_db


# Действия при запуске приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы, если их ещё нет
    Base.metadata.create_all(bind=engine)

    # Добавляем начальные устройства
    with SessionLocal() as db:
        crud.create_initial_devices(db)

    yield


# Создаём приложение FastAPI
app = FastAPI(
    title="Smart Home API",
    description="API для управления устройствами умного дома",
    version="1.0.0",
    lifespan=lifespan
)


# Разрешаем обращения с будущего React-сайта

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5180",
        "http://127.0.0.1:5180"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)



# Добавляем метрики для Prometheus
Instrumentator().instrument(app).expose(app)


# Главная страница API
@app.get("/")
def home():
    return {
        "message": "Smart Home API работает!"
    }


# Проверка работоспособности API
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Получение всех устройств
@app.get("/devices", response_model=dict[int, Device])
def get_devices(db: Session = Depends(get_db)):
    devices = crud.get_devices(db)

    return {
        device.id: device
        for device in devices
    }


# Включение и выключение устройства
@app.post(
    "/devices/{device_id}/toggle",
    response_model=ToggleResponse
)
def toggle_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = crud.toggle_device(db, device_id)

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Устройство не найдено"
        )

    return {
        "status": "success",
        "device": device
    }
