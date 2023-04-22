from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from src.database.ILogGateway import ILogGateway
from src.dto.LogInfo import LogInfo
from src.dto.ResponseLog import ResponseLog
from src.dto.SearchLogParameter import SearchLogParameter

import sqlalchemy
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, and_
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = "log"
    log_id: Mapped[int] = mapped_column(primary_key=True)
    remote_id: Mapped[str] = mapped_column(String(32))
    date: Mapped[str] = mapped_column(String(128))
    user_id: Mapped[int] = mapped_column(ForeignKey("client.user_id"))
    action: Mapped[str] = mapped_column(String(256))

    def __repr__(self) -> str:
        return f"Log(log_id={self.log_id!r}, remote_id={self.remote_id!r}, date={self.date!r}, action={self.action!r})"


class Client(Base):
    __tablename__ = "client"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    password_hash: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.name!r}, email={self.email!r})"


class LogDatabase(ILogGateway):
    def __init__(self):
        self.__db_engine = sqlalchemy.create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

    def save_log(self, log_info: LogInfo) -> None:
        with Session(self.__db_engine) as session:
            new_log = Log(
                remote_id=log_info.remote_id,
                date=log_info.date,
                user_id=log_info.user_id,
                action=log_info.action
            )

            session.add(new_log)
            session.commit()

    def get_logs(self, count: int, offset: int) -> List[ResponseLog]:
        with Session(self.__db_engine) as session:
            # query = session.query(Log.log_id,
            #                       Log.remote_id,
            #                       Log.date,
            #                       Log.user_id,
            #                       Log.action,
            #                       Client.name,
            #                       Client.email)\
            #     .join(Client, Log.user_id == Client.user_id) \
            #     .slice(0 + 5, count + 5)
            #     # .slice(0 + offset * count, count + offset * count)

            query = session.query(Log.log_id,
                                  Log.remote_id,
                                  Log.date,
                                  Log.user_id,
                                  Log.action,
                                  Client.name,
                                  Client.email) \
                .join(Client, Log.user_id == Client.user_id) \
                .filter(and_(0 + offset * count < Log.log_id, Log.log_id <= count + offset * count))

            response_log_list: List[ResponseLog] = []

            for row in query.limit(count).all():
                response_log_list.append(ResponseLog(
                    row.log_id,
                    row.remote_id,
                    row.date,
                    row.user_id,
                    row.action,
                    row.name,
                    row.email
                ))

            return response_log_list