from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField
from datetime import date
from wtforms import validators


class TeacherForm(Form):
    teacher_id = HiddenField()

    teacher_name = StringField("name: ", [
        validators.DataRequired("Please enter teacher`s name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    teacher_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter teacher`s faculty."),
        validators.Length(2, 255, "Text should be from 2 to 255 symbols")
    ])

    submit = SubmitField("Save")
