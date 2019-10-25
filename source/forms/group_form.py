from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField
from wtforms import validators
from datetime import date


class GroupForm(Form):
    group_id = HiddenField()

    group_name = StringField("name: ", [
        validators.DataRequired("Please enter group name."),
        validators.Length(3, 255, "Text should be from 3 to 255 symbols")
    ])

    group_faculty = StringField("faculty: ", [
        validators.DataRequired("Please enter group faculty."),
        validators.Length(2, 255, "Text should be from 2 to 255 symbols")])

    submit = SubmitField("Save")
