from flask_wtf import Form
from wtforms import SelectField, SubmitField, BooleanField
from sqlalchemy import func
from dao.db import PostgresDb
from dao.orm.entities import Group


class GroupSearchForm(Form):
    name = SelectField("name:", choices=[("", "---")])
    faculty = SelectField("faculty:", choices=[("", "---")])
    submit = SubmitField("Search")

    def init(self):
        db = PostgresDb()

        self.name.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Group.group_name).distinct(Group.group_name).all())]

        self.faculty.choices = [("", "---")] + [(i[0], i[0]) for i in list(
            db.sqlalchemy_session.query(Group.group_faculty).distinct(Group.group_faculty).all())]


    def search(self, method):
        db = PostgresDb()
        result, labels = [], []

        query = db.sqlalchemy_session.query(Group.group_faculty).distinct(Group.group_faculty)

        if method == 'POST':
            if self.faculty.data and self.faculty.data != "None":
                query = query.filter(Group.group_faculty == self.faculty.data)

        student_faculty_set = query.all()

        for faculty in student_faculty_set:

            query = db.sqlalchemy_session.query(Group.group_name, func.count(Group.group_name)).group_by(
                Group.group_name).filter(Group.group_faculty == faculty)

            if method == "POST":
                if self.group.data and self.group.data != "None":
                    query = query.filter(Group.group_name == self.group.data)
                if self.name.data and self.name.data != "None":
                    query = query.filter(Group.group_faculty == self.name.data)
            result.append(query.all())
            labels.append(f'faculty {faculty}')
        return result, labels
