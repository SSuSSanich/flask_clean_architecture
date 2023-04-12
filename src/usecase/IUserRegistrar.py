from src.dto.InputUserCredentials import InputUserCredentials


class IUserRegistrar:
    def register(self, user_data: InputUserCredentials) -> None:
        raise "not implemented interface method"