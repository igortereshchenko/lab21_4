from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, DateField, HiddenField, SelectField
from datetime import date
from wtforms import validators


class TableForm(Form):
    id = HiddenField()

    name = StringField("name: ")

    address = StringField("address: ")

    year = DateField("year: ", [
        validators.DataRequired("Please enter job salary.")], default=date.today())

    degree = StringField("degree: ", [validators.Length(1, 255, "degree should be from 1 to 255 symbols")])

    submit = SubmitField("Save")
