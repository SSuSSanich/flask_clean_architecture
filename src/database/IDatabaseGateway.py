from src.dto.InputUserCredentials import InputUserCredentials
from src.dto.OutputUserCredentials import OutputUserCredentials


class IDatabaseGateway:
    def save_user_credentials(self, user_data: InputUserCredentials) -> None:
        raise "not implemented interface method"

    def get_user_by_email_and_pass_hash(self, email: str, password: str) -> OutputUserCredentials:
        raise "not implemented interface method"