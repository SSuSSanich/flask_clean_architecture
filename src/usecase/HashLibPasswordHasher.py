import hashlib
from src.usecase.IPasswordHasher import IPasswordHasher


class HashLibPasswordHasher(IPasswordHasher):
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def hash(self, password: str) -> str:
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.__secret_key.encode('utf-8'),
            100000
        ).hex()