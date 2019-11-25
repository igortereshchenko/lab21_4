from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField, HiddenField, IntegerField, BooleanField
from django.core.exceptions import ValidationError
from datetime import date
from wtforms import validators


class CarForm(Form):

    model = StringField("model: ", [
        validators.DataRequired("Please enter car model.")
    ])

    color = StringField("color : ", [
        validators.DataRequired("Please enter car color.")
    ])

    def validate_on_submit(form, field):
        if field.data < 4:
            raise ValidationError('Length should be at least 4 numbers')

    numb = IntegerField("Car number ", [validators.DataRequired("Please enter car number: "), validate_on_submit])
    manuf = IntegerField("Car manuf ")
    teacher_id_fk = IntegerField("Teacher id ")
    old_model = HiddenField()

    submit = SubmitField("Save")