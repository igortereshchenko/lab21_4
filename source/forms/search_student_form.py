from flask_wtf import Form
from wtforms import SelectField, SubmitField, BooleanField
from sqlalchemy import func
from source.dao.db import PostgresDb
from source.dao.orm.entities import Student


class StudentSearchForm(Form):
    name = SelectField("name:", choices=[("", "---")])
    surname = SelectField("surname:", choices=[("", "---")])
    group = SelectField("group:", choices=[("", "---")])
    university = SelectField("university:", choices=[("", "---")])
    faculty = SelectField("faculty:", choices=[("", "---")])
    birthday = SelectField("birthday:", choices=[("", "---")])
    date_enrollment = SelectField("date_enrollment:", choices=[("", "---")])
    deleted = BooleanField("with deleted rows", default=True)
    submit = SubmitField("Search")

    def init(self):
        db = PostgresDb()

        self.name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_name).distinct(Student.student_name).all())]

        self.surname.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_surname).distinct(Student.student_surname).all())]

        self.group.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_group).distinct(Student.student_group).all())]

        self.university.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_university).distinct(Student.student_university).all())]

        self.faculty.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_faculty).distinct(Student.student_faculty).all())]

        self.birthday.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_birthday).distinct(Student.student_birthday).all())]

        self.date_enrollment.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Student.student_date_enrollment).distinct(
                Student.student_date_enrollment).all())]

    def search(self, method):
        db = PostgresDb()
        result, labels = [], []

        query = db.sqlalchemy_session.query(Student.student_university, Student.student_faculty).distinct(
            Student.student_university, Student.student_faculty)

        if method == 'POST':
            if self.university.data and self.university.data != "None":
                query = query.filter(Student.student_university == self.university.data)
            if self.faculty.data and self.faculty.data != "None":
                query = query.filter(Student.student_faculty == self.faculty.data)

        student_uni_and_faculty_set = query.all()

        for uni, faculty in student_uni_and_faculty_set:

            query = db.sqlalchemy_session.query(Student.student_group, func.count(Student.student_group)).group_by(
                Student.student_group).filter(Student.student_university == uni, Student.student_faculty == faculty)

            if method == "POST":
                if self.group.data and self.group.data != "None":
                    query = query.filter(Student.student_group == self.group.data)
                if self.name.data and self.name.data != "None":
                    query = query.filter(Student.student_name == self.name.data)
                if self.surname.data and self.surname.data != "None":
                    query = query.filter(Student.student_surname == self.surname.data)
                if self.birthday.data and self.birthday.data != "None":
                    query = query.filter(Student.student_birthday == self.birthday.data)
                if self.date_enrollment.data and self.date_enrollment.data != "None":
                    query = query.filter(Student.student_date_enrollment == self.date_enrollment.data)
                if not bool(self.deleted.data) and self.deleted.data != "None":
                    query = query.filter(Student.student_date_expelled == None)
            result.append(query.all())
            labels.append(f'university {uni}, faculty {faculty}')
        return result, labels
