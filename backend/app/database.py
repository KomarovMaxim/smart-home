
import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Получаем адрес базы данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Не задана переменная окружения DATABASE_URL"
    )


# Создаём подключение к PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Фабрика сессий для работы с базой
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


# Базовый класс таблиц SQLAlchemy
class Base(DeclarativeBase):
    pass


# Предоставляем подключение для каждого API-запроса
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
