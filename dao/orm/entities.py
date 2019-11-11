from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
import datetime



Base = declarative_base()


class Group(Base):
    __tablename__ = 'Groups'

    group_id = Column(Integer, primary_key=True)
    group_faculty = Column(String(255), nullable=False)
    group_name = Column(String(255), nullable=False)

    group_record = relationship("Scedule")


class Teacher(Base):
    __tablename__ = 'Teachers'

    teacher_id = Column(Integer, primary_key=True)
    teach_name = Column(String(255), nullable=False)
    teach_faculty = Column(String(255), nullable=False)


class Subject(Base):
    __tablename__ = 'Subjects'

    subj_faculty = Column(String(255),primary_key=True)
    subj_name = Column(String(255), primary_key=True)
    subj_hours = Column(Integer, nullable=True)


class Student(Base):
    __tablename__ = 'Student'

    stud_name = Column(String(255),primary_key=True)
    gender = Column(Boolean, nullable=True)
    counter = Column(Integer, nullable=True)
    group_ids_fk = Column(Integer, nullable=True)


class Scedule(Base):
    __tablename__ = 'Scedule'

    group_id_fk = Column(Integer, ForeignKey('Groups.group_id'), primary_key=True)
    subj_name_fk = Column(String(255), primary_key=True)
    subj_faculty_fk = Column(String(255), primary_key=True)
    teach_id_fk = Column(Integer, ForeignKey('Teachers.teacher_id'), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([subj_name_fk, subj_faculty_fk],
                                           [Subject.subj_name, Subject.subj_faculty]), {})

    subject_entity = relationship("Subject")
    teacher_entity = relationship("Teacher")


class Univer(Base):
    __tablename__ = 'Univer'

    name = Column(String(255),primary_key=True)
    addr = Column(String(255), nullable=True)
    counter = Column(Integer, nullable=True)
    teacher_id_fk = Column(Integer, ForeignKey('Teachers.teacher_id'), nullable=True)

    teacher_entity = relationship("Teacher")


class Work1(Base):
    __tablename__ = 'Work1'

    name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    subj_name_fk = Column(String(255), primary_key=True)
    subj_faculty_fk = Column(String(255), primary_key=True)
    salary = Column(Integer, nullable=True)
    open_date = Column(Date, nullable=True)
    __table_args__ = (ForeignKeyConstraint([subj_name_fk, subj_faculty_fk],
                                           [Subject.subj_name, Subject.subj_faculty]), {})

    subject_entity = relationship("Subject")


if __name__ == '__main__':
    from dao.db import PostgresDb

    db = PostgresDb()
    # simple query test
    q1 = db.sqlalchemy_session.query(Subject).all()
    q2 = db.sqlalchemy_session.query(Scedule).all()

    a = db.sqlalchemy_session.query(Group).join(Scedule).join(Subject).join(Teacher).all()
    print()
