from dao.db import PostgresDb
from dao.orm.entities import *

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

# clear all tables in right order
# session.query(OrmFileEditor).delete()
# session.query(OrmFile).delete()
# session.query(OrmUser).delete()

# populate database with new rows

AM = Subject(subject_faculty='AM',
                 subject_name='Math',
                 subject_hours=3)

# insert into database
session.add_all([AM])

session.commit()
