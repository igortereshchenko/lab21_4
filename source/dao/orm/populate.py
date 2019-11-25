from source.dao.orm.entities import *
import datetime
from source.dao.db import PostgresDb
import random


def populate():
    db = PostgresDb()

    session = db.sqlalchemy_session

    commit = []

    students = list(db.sqlalchemy_session.query(Student).all())

    for student in students:
        professors = list(db.sqlalchemy_session.query(Professor.professor_id).filter(
            Professor.professor_university == student.student_university).all())

        disciplines = list(
            db.sqlalchemy_session.query(Discipline).filter(
                Discipline.discipline_university == student.student_university,
                Discipline.discipline_faculty == student.student_faculty).all())

        if len(disciplines) == 0 or len(professors) == 0:
            continue

        index = random.randint(0, len(professors) - 1)
        professor = professors[index]
        index = random.randint(0, len(disciplines) - 1)
        discipline = disciplines[index]
        semester = int(random.normalvariate(45, 5))
        final = int(random.normalvariate(75, 15))
        commit.append(StudentRecordBook(
            student_id_fk=student.student_id,
            discipline_name_fk=discipline.discipline_name,
            discipline_faculty_fk=discipline.discipline_faculty,
            discipline_university_fk=discipline.discipline_university,
            professor_id_fk=professor[0],
            semester_mark=semester,
            final_mark=final,
            exam_passed=datetime.date.today()
        ))

    # insert into database
    session.add_all(commit)
    session.commit()

db = PostgresDb()

session = db.sqlalchemy_session

commit = []

students = list(db.sqlalchemy_session.query(Student).all())

for student in students:
    professors = list(db.sqlalchemy_session.query(Professor.professor_id).filter(
        Professor.professor_university == student.student_university).all())

    disciplines = list(
        db.sqlalchemy_session.query(Discipline).filter(
            Discipline.discipline_university == student.student_university,
            Discipline.discipline_faculty == student.student_faculty).all())

    if len(disciplines) == 0 or len(professors) == 0:
        continue

    index = random.randint(0, len(professors) - 1)
    professor = professors[index]
    index = random.randint(0, len(disciplines) - 1)
    discipline = disciplines[index]
    semester = int(random.normalvariate(45, 5))
    final = int(random.normalvariate(75, 15))
    commit.append(StudentRecordBook(
        student_id_fk=student.student_id,
        discipline_name_fk=discipline.discipline_name,
        discipline_faculty_fk=discipline.discipline_faculty,
        discipline_university_fk=discipline.discipline_university,
        professor_id_fk=professor[0],
        semester_mark=semester,
        final_mark=final,
        exam_passed=datetime.date.today()
    ))

# insert into database
session.add_all(commit)
session.commit()
