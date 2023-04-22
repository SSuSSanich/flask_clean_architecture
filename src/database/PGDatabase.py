from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.InputUserCredentials import InputUserCredentials
from src.dto.OutputUserCredentials import OutputUserCredentials
import sqlalchemy
from sqlalchemy import text

from src.exception.EmailExistenceError import EmailExistenceError
from src.exception.UserExistenceError import UserExistenceError

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class PGDatabase(IDatabaseGateway):
    def __init__(self):
        self.__db_engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
        self.__db_connection = self.__db_engine.connect()  # коннектить при вызове или в init?

    def save_user_credentials(self, user_data: InputUserCredentials) -> None:
        if self.__is_email_exists(user_data.email):
            raise EmailExistenceError("The user already exist")

        self.__db_connection.execute(text(f"INSERT INTO client (name, password_hash, email)"
                                          f" VALUES (\'{user_data.name}\', \'{user_data.password}\', \'{user_data.email}\');"))
        self.__db_connection.commit()

    def __is_email_exists(self, email) -> bool:
        result = self.__db_connection.execute(
            text(f"SELECT email FROM client WHERE email = '{email}';"))
        user_data = result.fetchall()

        if len(user_data) == 0:
            return False

        return True

    def get_user_by_email_and_pass_hash(self, email: str, password: str) -> OutputUserCredentials:
        result = self.__db_connection.execute(
            text(f"SELECT * FROM client WHERE email = '{email}' AND password_hash = '{password}';"))
        user_data = result.fetchall()
        if len(user_data) == 0:
            raise UserExistenceError("The incorrect username or password")

        user_data = user_data[0]

        user_id = user_data[0]
        user_name = user_data[1]
        user_password = user_data[2]
        user_email = user_data[3]

        if len(user_email) == 0:
            raise "User is not found"

        output_user_credentials = OutputUserCredentials(
            user_id,
            user_name,
            user_password,
            user_email
        )

        return output_user_credentials
