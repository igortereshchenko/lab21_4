from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, BooleanField
from datetime import date
from wtforms import validators


class SubjectForm(Form):

    subject_name = StringField("name: ", [
        validators.DataRequired("Please enter subject`s name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    subject_faculty = StringField("faculty : ", [
        validators.DataRequired("Please enter subject`s faculty."),
        validators.Length(2, 255, "Text should be from 2 to 255 symbols")
    ])

    subject_hours = IntegerField("Hours per week: ")

    submit = SubmitField("Save")
