from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.InputUserCredentials import InputUserCredentials
from src.dto.OutputUserCredentials import OutputUserCredentials


class FileDatabase(IDatabaseGateway):
    def save_user_credentials(self, user_data: InputUserCredentials) -> None:
        users_collection = open("./saved_users", 'a')
        users_collection.write(user_data.name + ' ' + user_data.password + ' ' + user_data.email + '\n')
        users_collection.close()

    def get_user_by_email_and_pass_hash(self, email: str, password: str) -> OutputUserCredentials:
        raise "not implemented method"