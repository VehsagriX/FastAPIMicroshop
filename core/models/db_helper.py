from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from asyncio import current_task

from core.config import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engin = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engin,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        async_scoped_session — это обёртка, которая даёт отдельную сессию для каждого асинхронного запроса.
        scopefunc = current_task — говорит: "каждый asyncio-task должен иметь свою уникальную сессию".
        Это полезно, чтобы запросы не мешали друг другу (например, если к серверу пришло сразу 5 запросов).
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Реализация через sessipn_factory
        Это асинхронный генератор, который FastAPI может использовать как зависимость (Depends)
        Даёт сессию (yield session) во время выполнения запроса.
        Потом автоматически удаляет сессию (await session.close()), когда запрос завершён (или если ошибка).
        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scope_session_dependency(self) -> AsyncSession:
        """Реализация через async_scoped_session"""
        session = self.get_scoped_session()
        yield session
        await session.remove()


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.echo,
)
