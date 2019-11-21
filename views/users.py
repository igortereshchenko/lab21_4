from wtforms import StringField, DateTimeField, IntegerField, SubmitField, validators
from flask_wtf import FlaskForm
from domain import models


class UsersViewModel(FlaskForm):

    Login = StringField("Login: ", [validators.DataRequired("Please enter your Login.")])
    Password = StringField("Password: ", [validators.DataRequired("Please enter your Password.")])
    Email = StringField("Email: ", [validators.DataRequired("Please enter your Email.")])
    Lastname = StringField("Lastname: ", [validators.DataRequired("Please enter your Lastname.")])
    Firstname = StringField("Firstname: ", [validators.DataRequired("Please enter your Firstname.")])
    Age = IntegerField("Age: ", [validators.DataRequired("Please enter your Age.")])
    Eyes = StringField("Eyes: ", [validators.DataRequired("Please enter your Eyes.")])
    Hair = StringField("Hair: ", [validators.DataRequired("Please enter your Hair.")])
    Height = IntegerField("Height: ", [validators.DataRequired("Please enter your Height.")])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Users(
            Login=self.Login.data,
            Password=self.Password.data,
            Email=self.Email.data,
            Lastname=self.Lastname.data,
            Firstname=self.Firstname.data,
            Age=self.Age.data,
            Eyes=self.Eyes.data,
            Hair=self.Hair.data,
            Height=self.Height.data,
            CreatedOn=self.CreatedOn.data
        )