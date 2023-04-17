from src.database.SQLAlchemyPGDatabase import SQLAlchemyPGDatabase

if __name__ == "__main__":
    sqlAlchemyPGDatabase = SQLAlchemyPGDatabase()
    sqlAlchemyPGDatabase.get_user_by_email_and_pass_hash("drifttd@gmail.com", "password")