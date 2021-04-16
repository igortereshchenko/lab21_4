from sqlalchemy import Column, Integer, String, Date, ForeignKey, ForeignKeyConstraint, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    Company = Column(String, primary_key = True, nullable=False)


class User(Base):
    __tablename__ = 'user'
    Username = Column(String, primary_key = True, nullable=False)
    Password = Column(String, nullable=False)
    Company = Column(String)


class Message(Base):
    __tablename__ = 'message'
    MessageID = Column(Integer, primary_key = True, nullable=False)
    MessageSender = Column(String, ForeignKey('user.Username'))
    MessageContent = Column(String)
    MessageDate = Column(Date)

class Messenger(Base):
    __tablename__ = 'messenger'
    Site = Column(String, primary_key = True, nullable=False)
    Version = Column(String)
    Country = Column(String)
    Price = Column(Integer, nullable=False)
    Username = Column(String, ForeignKey('user.Username'), nullable=False)