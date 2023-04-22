import sqlalchemy
from sqlalchemy.orm import Session

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.InputUserCredentials import InputUserCredentials
from src.dto.OutputUserCredentials import OutputUserCredentials
from src.exception.EmailExistenceError import EmailExistenceError
from src.exception.UserExistenceError import UserExistenceError

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    password_hash: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.name!r}, email={self.email!r})"


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class SQLAlchemyPGDatabase(IDatabaseGateway):
    def __init__(self):
        self.__db_engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

    def save_user_credentials(self, user_data: InputUserCredentials) -> None:
        if self.__is_email_exists(user_data.email):
            raise EmailExistenceError("The user already exist")

        with Session(self.__db_engine) as session:
            new_user = Client(
                name=user_data.name,
                password_hash=user_data.password,
                email=user_data.email
            )

            session.add(new_user)
            session.commit()

    def __is_email_exists(self, email) -> bool:
        session = Session(self.__db_engine)

        stmt = sqlalchemy.select(Client).where(sqlalchemy.and_(Client.email == email))
        user_data = session.scalars(stmt).first()
        if not user_data:
            return False
        return True

    def get_user_by_email_and_pass_hash(self, email: str, password: str) -> OutputUserCredentials:
        session = Session(self.__db_engine)

        stmt = sqlalchemy.select(Client).where(sqlalchemy.and_(Client.email == email,
                                                               Client.password_hash == password))
        user_data = session.scalars(stmt).first()

        if not user_data:
            raise UserExistenceError("The incorrect username or password")

        output_user_credentials = OutputUserCredentials(
            user_data.user_id,
            user_data.name,
            user_data.password_hash,
            user_data.email
        )

        return output_user_credentials
