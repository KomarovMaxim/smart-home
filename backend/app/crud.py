
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import DeviceDB


# Добавляем начальные устройства в пустую базу
def create_initial_devices(db: Session):
    existing_device = db.scalar(
        select(DeviceDB.id).limit(1)
    )

    if existing_device is not None:
        return

    devices = [
        DeviceDB(
            id=1,
            name="Умный свет",
            status="off"
        ),
        DeviceDB(
            id=2,
            name="Термостат",
            status="on"
        )
    ]

    db.add_all(devices)
    db.commit()


# Получаем список устройств
def get_devices(db: Session):
    statement = select(DeviceDB).order_by(DeviceDB.id)

    return list(db.scalars(statement).all())


# Включаем или выключаем устройство
def toggle_device(db: Session, device_id: int):
    device = db.get(DeviceDB, device_id)

    if device is None:
        return None

    if device.status == "off":
        device.status = "on"
    else:
        device.status = "off"

    db.commit()
    db.refresh(device)

    return device
