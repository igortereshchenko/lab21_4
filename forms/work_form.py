from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, BooleanField
from datetime import date
from wtforms import validators


class Work1Form(Form):

    name = StringField("name: ", [
        validators.DataRequired("Please enter worker`s name.")
    ])

    company = StringField("company : ", [
        validators.DataRequired("Please enter company.")
    ])

    salary = IntegerField("Worker`s salary ")
    open_date = DateField("Open date ")
    subj_name_fk = StringField("subj_name_fk : ", [
        validators.DataRequired("Please enter subject name.")
    ])
    subj_faculty_fk = StringField("subj_faculty_fk : ", [
        validators.DataRequired("Please enter subject faculty.")
    ])
    old_subj_name_fk = HiddenField()
    old_subj_faculty_fk = HiddenField()

    submit = SubmitField("Save")