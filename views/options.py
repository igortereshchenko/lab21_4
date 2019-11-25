from wtforms import StringField, DateTimeField, IntegerField, SubmitField, validators, SelectField
from flask_wtf import FlaskForm
from domain import models


class OptionsViewModel(FlaskForm):
    Place = StringField("Place: ", [validators.DataRequired("Please enter optoins Place.")])
    Season = StringField("Season: ", [validators.DataRequired("Please enter optoins Season.")])
    Temperature = IntegerField("Temperature: ", [validators.DataRequired("Please enter optoins Temperature.")])
    Event = SelectField("Event ", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Options(
            Place=self.Place.data,
            Season=self.Season.data,
            Temperature=self.Temperature.data,
            CreatedOn=self.CreatedOn.data,
            event_idIdFk=self.Event.data
        )
