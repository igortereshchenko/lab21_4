from wtforms import StringField, DateTimeField, SubmitField, validators, SelectField
from flask_wtf import FlaskForm
from domain import models


class ClothesViewModel(FlaskForm):
    Outwear = StringField("Outwear: ", [validators.DataRequired("Please enter clothes Outwear.")])
    Lowerwear = StringField("Lowerwear: ", [validators.DataRequired("Please enter clothes Lowerwear.")])
    Shoes = StringField("Shoes: ", [validators.DataRequired("Please enter clothes Shoes.")])
    Option = SelectField("Option ", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Clothes(
            Outwear=self.Outwear.data,
            Lowerwear=self.Lowerwear.data,
            Shoes=self.Shoes.data,
            CreatedOn=self.CreatedOn.data,
            option_idIdFk=self.Option.data
        )
