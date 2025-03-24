from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt
from src.exceptions import IncorrectTokenException, EmailNotRegisteredException, IncorrectPasswordException, \
    ObjectAlreadyExistsException, UserAlreadyExistsException, PasswordEmptyException, EmptyValueException
from src.schemas.users import UserRequestAdd, UserAdd
from src.config import settings
from src.services.base import BaseServiceLayer

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService(BaseServiceLayer):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )  # время жизни токена
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, pwd: str) -> str:
        return self.pwd_context.hash(pwd)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_jwt_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException


    async def register_user(self, data: UserRequestAdd):
        try:
            if data.password != '':
                hashed_password = self.hash_password(data.password)
            else:
                raise EmptyValueException
        except EmptyValueException as ex:
            raise PasswordEmptyException

        # hashed_password = self.hash_password(data.password)

        # new_user_data = UserAdd(email=data.email, password=hashed_password, name=data.name)
        new_user_data = UserAdd(email=data.email, password=hashed_password, name='')
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex


    async def login_user(self, data: UserRequestAdd) -> str:
        user = await self.db.users.get_user_hash_pwd(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        # проверим пароль юзера
        if not self.verify_password(data.password, user.password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token


    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)