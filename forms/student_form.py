from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, BooleanField
from datetime import date
from wtforms import validators


class StudentForm(Form):

    name = StringField("name: ", [
        validators.DataRequired("Please enter student`s name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    record_book = StringField("record_book : ", [
        validators.DataRequired("Please enter the number of record_book."),
        validators.Length(2, 255, "Text should be from 2 to 255 symbols")
    ])

    gender = BooleanField("Gender: ")

    submit = SubmitField("Save")