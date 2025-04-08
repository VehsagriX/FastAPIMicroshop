from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

# Это делается, чтоб избежать ошибки циклических импортов
if TYPE_CHECKING:  # Если сейчас проверка типов, то импортируй
    from .user import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, default="", server_default=""
    )  # в базе будет значение по умолчанию

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    user: Mapped["User"] = relationship("User", back_populates="posts")
