from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, ForeignKeyConstraint
from dao.orm.entities import *

Base = declarative_base()
class Dish(Base):
    __tablename__ = 'dish'
    dishname = Column(String(80), primary_key=True)
    calories_amount = Column(Integer, nullable=False)

class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    typename = Column(String(80))
    dishname_fk = Column(String(100), ForeignKey('dish.dishname'))


class Receipt(Base):
    __tablename__ = 'receipt'
    dishname_fk = Column(String(100), ForeignKey('dish.dishname'))
    receipt_content = Column(String(100), primary_key=True)


class Ingridients(Base):
    __tablename__ = 'ingridient'
    ingridientname = Column(String(80), primary_key=True)


class Dish_Type(Base):
    __tablename__ = 'dish_type'
    dishname = Column(String(255), ForeignKey('Dish.dishname'), primary_key=True)
    type = Column(String(255), primary_key=True)

class Restaurant(Base):
    __tablename__ = 'restaurant'
    address = Column(String(80))
    city = Column(String(80))
    star = Column(Integer, nullable=False)
    country = Column(String(80))
    name = Column(String, primary_key=True)
    dishname_fk = Column(String(80))




    dishname_fk = Column(String(100), ForeignKey('dish.dishname'))
