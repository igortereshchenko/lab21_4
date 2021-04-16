from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField
from wtforms import validators


class UserForm(Form):
    __tablename__ = 'user'
   
    Username = StringField("User : ", [
        validators.DataRequired("Please, enter Username."),
        validators.Length(3, 20, "Username should be from 3 to 20 symbols")])
    
    Password = StringField("Password : ", [
        validators.DataRequired("Please enter the Password."),
        validators.Length(3, 20, "Password should be from 3 to 20 symbols")])
    
    Company = StringField("Company Name: ", [
        validators.DataRequired("Please enter the Company Name."),
        validators.Length(3, 20, "Company Name should be from 3 to 20 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")


class CompaniesForm(Form):
    __tablename__ = 'company'
   
    Company = StringField("Company Name: ", [
        validators.DataRequired("Please enter Company Name."),
        validators.Length(3, 20, "Company Name should be from 3 to 20 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")


class MessagesForm(Form):
    __tablename__ = 'message'

    MessageSender = StringField("Message Sender: ", [
        validators.DataRequired("Please enter Message Sender."),
        validators.Length(3, 20, "Message Sender should be from 3 to 20 symbols")])
    
    MessageContent = StringField("Message Content: ", [
        validators.DataRequired("Please enter Content of the message."),
        validators.Length(3, 80, "Message content should be from 1 to 2000 symbols")])
    
    # 2000-12-31 - sample of date input
    # MessageDate = DateField("Message Date: ", [
    #     validators.DataRequired("Please enter Message Date.")])
    
    old_name = HiddenField()
    submit = SubmitField("Save")

    
class MessengerForm(Form):
    __tablename__ = 'messenger'

    Site = StringField("Site: ", [
        validators.DataRequired("Site."),
        validators.Length(10, 240, "Site should be from 10 to 240 symbols")])
    
    Version = StringField("Version: ", [
        validators.DataRequired("Version."),
        validators.Length(3, 20, "Version should be from 3 to 20 symbols")])
    
    Country = StringField("Country: ", [
        validators.DataRequired("Country."),
        validators.Length(3, 20, "Country should be from 3 to 20 symbols")])
    
    Price = IntegerField("Price: ",        
        [validators.DataRequired("Price."),
        validators.number_range(0,100)])

    Username = StringField("Username: ", [
        validators.DataRequired("Username."),
        validators.Length(0, 100, "Username should be from 3 to 20 symbols")])
    
    old_name = HiddenField()
    submit = SubmitField("Save")