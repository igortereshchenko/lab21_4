import os

username = 'postgres'
password = 'eugene'
host = '127.0.0.1'
port = '5432'
database = 'postgres'
DATABASE_URI = os.getenv("DATABASE_URL",
                         'postgres+psycopg2://postgres:{}@{}:{}/{}'.format(password, host, port, database))
