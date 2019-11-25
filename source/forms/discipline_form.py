from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms import validators


class DisciplineForm(Form):

    discipline_university = StringField("university: ", [
        validators.DataRequired("Please enter discipline university."),
        validators.Length(3, 255, "Name should be from 3 to 255 symbols")
    ])

    discipline_faculty = StringField("faculty : ", [
        validators.DataRequired("Please enter discipline faculty."),
        validators.Length(3, 255, "Type should be from 3 to 255 symbols")
    ])

    discipline_name = StringField("name: ", [
        validators.DataRequired("Please enter discipline name."),
        validators.Length(3, 255, "Context should be from 3 to 255 symbols")])

    discipline_exam = BooleanField("exam: ")

    discipline_hours_for_semester = IntegerField("hours for semester: ")

    submit = SubmitField("Save")
