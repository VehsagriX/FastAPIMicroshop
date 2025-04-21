from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base
from .mixins import UserRelationMixin


# Это делается, чтоб избежать ошибки циклических импортов
# if TYPE_CHECKING: # Если сейчас проверка типов, то импортируй
#     from .user import User


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, default="", server_default=""
    )  # в базе будет значение по умолчанию

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id!r})"

    def __repr__(self):
        return str(self)
