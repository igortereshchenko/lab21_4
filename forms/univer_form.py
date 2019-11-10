from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, BooleanField
from datetime import date
from wtforms import validators


class UniverForm(Form):

    name = StringField("name: ", [
        validators.DataRequired("Please enter univer name.")
    ])

    addr = StringField("addr : ", [
        validators.DataRequired("Please enter univer addr.")
    ])

    counter = IntegerField("Teacher salary ")
    teacher_id_fk = IntegerField("Teacher id ")
    old_name = HiddenField()

    submit = SubmitField("Save")
