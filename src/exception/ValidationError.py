class ValidationError(Exception):
    def __init__(self, info: str):
        self.__info = info

    def __repr__(self):
        return self.__info