from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True  # абстрактная модель не создается в базе такая таблица

    @declared_attr.directive
    def __tablename__(cls):
        """Автоматически генерирует имя таблицы"""
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
