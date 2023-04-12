from src.dto.LoginInformation import LoginInformation
from src.dto.OutputUserCredentials import OutputUserCredentials


class IUserLogger:
    def login(self, login_info: LoginInformation) -> OutputUserCredentials:
        raise "not implemented interface method"
