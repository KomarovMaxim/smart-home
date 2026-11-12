
import os

# Тестовая база данных в памяти
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+pysqlite:///:memory:"
)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app import crud
from app import models


def test_devices():
    # Создаём временную базу данных
    engine = create_engine(
        "sqlite+pysqlite:///:memory:"
    )

    Base.metadata.create_all(bind=engine)

    try:
        with Session(engine) as db:
            # Создание устройств
            crud.create_initial_devices(db)

            # Проверка количества устройств
            devices = crud.get_devices(db)
            assert len(devices) == 2

            # Проверка умного света
            light = next(
                d for d in devices if d.id == 1
            )

            assert light.name == "Умный свет"
            assert light.status == "off"

            # Включение света
            result = crud.toggle_device(db, 1)
            assert result.status == "on"

            # Выключение света
            result = crud.toggle_device(db, 1)
            assert result.status == "off"

            # Несуществующее устройство
            assert crud.toggle_device(db, 999) is None

    finally:
        engine.dispose()
