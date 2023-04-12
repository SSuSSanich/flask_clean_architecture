from src.exception.ValidationError import ValidationError
from src.usecase.IValidator import IValidator


class SimpleValidator(IValidator):
    def __init__(self):
        self.forbidden_letters: tuple = ('\'', '#', '\\', '/')
        self.necessary_letters: tuple = ('@', '.')

    def check_name(self, name: str) -> None:
        if len(name) < 3:
            raise ValidationError("The name's length is to short")
        for letter in self.forbidden_letters:
            if name.find(letter) > 0:
                raise ValidationError(f"The name has a forbidden letter {letter}")

    def check_password(self, password: str) -> None:
        if len(password) < 5:
            raise ValidationError("The password's length is to short")
        for letter in self.forbidden_letters:
            if password.find(letter) > 0:
                raise ValidationError(f"The password has a forbidden letter {letter}")

    def check_email(self, email: str) -> None:
        if len(email) < 6:
            raise ValidationError("The email's length is to short")
        for letter in self.forbidden_letters:
            if email.find(letter) > 0:
                raise ValidationError(f"The email has a forbidden letter {letter}")
        for letter in self.necessary_letters:
            if email.find(letter) < 0:
                raise ValidationError("The email has not necessary letters")
