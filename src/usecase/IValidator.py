class IValidator:
    def check_name(self, name: str) -> None:
        raise "not implemented interface method"

    def check_password(self, password: str) -> None:
        raise "not implemented interface method"

    def check_email(self, email: str) -> None:
        raise "not implemented interface method"