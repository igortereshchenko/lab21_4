from credentials import *
from sqlalchemy import create_engine


class Database():
    connection = create_engine(f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}")

    def __init__(self):
        self.connection = self.connection.connect()
        print("kolobayeva")


if __name__ == "__main__":
    db_con = Database()
