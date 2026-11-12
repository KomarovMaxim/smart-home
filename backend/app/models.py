
from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


# Таблица устройств в PostgreSQL
class DeviceDB(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )


# Модель устройства для FastAPI
class Device(BaseModel):
    id: int
    name: str
    status: Literal["on", "off"]

    model_config = ConfigDict(from_attributes=True)


# Ответ после переключения устройства
class ToggleResponse(BaseModel):
    status: str
    device: Device
