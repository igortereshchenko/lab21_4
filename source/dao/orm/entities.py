from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = 'Student'

    student_id = Column(Integer, primary_key=True)
    student_university = Column(String(255), nullable=False)
    student_faculty = Column(String(255), nullable=False)
    student_group = Column(String(255), nullable=False)
    student_name = Column(String(255), nullable=False)
    student_surname = Column(String(255), nullable=False)
    student_birthday = Column(Date, nullable=True)
    student_date_enrollment = Column(Date, nullable=False, default=datetime.date.today())
    student_date_expelled = Column(Date, nullable=True)

    student_record = relationship("StudentRecordBook")


class Professor(Base):
    __tablename__ = 'Professor'

    professor_id = Column(Integer, primary_key=True)
    professor_university = Column(String(255), nullable=False)
    professor_department = Column(String(255), nullable=False)
    professor_name = Column(String(255), nullable=False)
    professor_surname = Column(String(255), nullable=False)
    professor_birthday = Column(Date, nullable=True)
    professor_date_enrollment = Column(Date, nullable=False, default=datetime.date.today())
    professor_date_expelled = Column(Date, nullable=True)
    professor_degree = Column(String(255), nullable=True)


class Univer(Base):
    __tablename__ = 'Univer'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    year = Column(Date)
    degree = Column(String(255))


class Discipline(Base):
    __tablename__ = 'Discipline'

    discipline_university = Column(String(255), primary_key=True)
    discipline_faculty = Column(String(255), primary_key=True)
    discipline_name = Column(String(255), primary_key=True)
    discipline_exam = Column(Boolean, nullable=False)
    discipline_hours_for_semester = Column(Integer, nullable=True)
    univ_fk = Column(Integer, ForeignKey('Univer.id'))


class StudentRecordBook(Base):
    __tablename__ = 'StudentRecordBook'

    student_id_fk = Column(Integer, ForeignKey('Student.student_id'), primary_key=True)
    discipline_name_fk = Column(String(255), primary_key=True)
    discipline_faculty_fk = Column(String(255), primary_key=True)
    discipline_university_fk = Column(String(255), primary_key=True)
    professor_id_fk = Column(Integer, ForeignKey('Professor.professor_id'), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([discipline_name_fk, discipline_faculty_fk, discipline_university_fk],
                                           [Discipline.discipline_name, Discipline.discipline_faculty,
                                            Discipline.discipline_university]),
                      {})

    semester_mark = Column(Integer, nullable=True)
    final_mark = Column(Integer, nullable=True)
    exam_passed = Column(Date, nullable=True)

    student_entity = relationship("Student")
    discipline_entity = relationship("Discipline")
    professor_entity = relationship("Professor")


if __name__ == '__main__':
    from source.dao.db import PostgresDb

    db = PostgresDb()
    # simple query test
    q1 = db.sqlalchemy_session.query(Discipline).all()
    q2 = db.sqlalchemy_session.query(StudentRecordBook).all()

    a = db.sqlalchemy_session.query(Student).join(StudentRecordBook).join(Discipline).join(Professor).all()
    print()
