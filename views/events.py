from wtforms import StringField, DateTimeField, IntegerField, SubmitField, SelectField, validators
from flask_wtf import FlaskForm
from domain import models


class EventsViewModel(FlaskForm):
    Event_name = StringField("Name: ", [validators.DataRequired("Please enter events Name.")])

    User = SelectField("User", validators=[validators.DataRequired()])

    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Events(
            Event_name=self.Event_name.data,
            CreatedOn=self.CreatedOn.data,
            user_idIdFk=self.User.data
        )