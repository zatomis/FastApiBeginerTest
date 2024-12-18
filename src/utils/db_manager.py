#для того чтобы уйти от контекстных менеджеров и сделать свой
from src.repositories.hotels import HotelRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository
from src.schemas.hotels import Hotel


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self): #метод конт.менеджера - для входа
        self.session = self.session_factory()
        #тут держим наши репозитории
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)
        return self

    async def __aexit__(self, *args): #метод конт.менеджера - для выхода
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        return self.session.commit()
