from pydantic import EmailStr
from sqlalchemy import select

from src.database import engine
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserWithHashPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_hash_pwd(self, email: EmailStr):
        query_statement = select(self.model).filter_by(email=email)
        print(
            query_statement.compile(
                engine, compile_kwargs={"literal_binds": True}
            )
        )
        query_result = await self.session.execute(query_statement)
        model = query_result.scalars().one()
        return UserWithHashPassword.model_validate(model, from_attributes=True)
