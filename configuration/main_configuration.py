from src.database.IDatabaseGateway import IDatabaseGateway
from src.database.PGDatabase import PGDatabase
from src.database.SQLAlchemyPGDatabase import SQLAlchemyPGDatabase
from src.usecase.HashLibPasswordHasher import HashLibPasswordHasher
from src.usecase.IPasswordHasher import IPasswordHasher
from src.usecase.IUserLogger import IUserLogger
from src.usecase.IUserRegistrar import IUserRegistrar
from src.usecase.IValidator import IValidator
from src.usecase.SimpleUserLogger import SimpleUserLogger
from src.usecase.SimpleUserRegistrar import SimpleUserRegistrar
from src.usecase.SimpleValidator import SimpleValidator

from config import HASH_SECRET_KEY

database: IDatabaseGateway = SQLAlchemyPGDatabase()
validator: IValidator = SimpleValidator()
password_hasher: IPasswordHasher = HashLibPasswordHasher(HASH_SECRET_KEY)
user_registrar: IUserRegistrar = SimpleUserRegistrar(validator, database, password_hasher)
user_logger: IUserLogger = SimpleUserLogger(database, validator, password_hasher)