from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime
from views.users import UsersViewModel
from views.events import EventsViewModel
from views.options import OptionsViewModel
from views.clothes import ClothesViewModel

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column("user_id", db.Integer, primary_key=True)
    Login = db.Column("login", db.String, nullable=False)
    Password = db.Column("password", db.String, nullable=False)
    Email = db.Column("email", db.String, nullable = False)
    Lastname = db.Column("lastname", db.String)
    Firstname = db.Column("firstname", db.String)
    Age = db.Column("age", db.Integer)
    Eyes = db.Column("eyes", db.String)
    Hair = db.Column("hair", db.String)
    Height = db.Column("height", db.Integer)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.now)

    def wtf(self):
        return UsersViewModel(
            Login=self.Login,
            Password=self.Password,
            Email=self.Email,
            Lastname=self.Lastname,
            Firstname=self.Firstname,
            Age=self.Age,
            Eyes=self.Eyes,
            Hair=self.Hair,
            Height=self.Height,
            CreatedOn=self.CreatedOn
        )

    def map_from(self, form):
        self.Login = form.Login.data,
        self.Password = form.Password.data,
        self.Email = form.Email.data,
        self.Lastname = form.Lastname.data,
        self.Firstname = form.Firstname.data,
        self.Age = form.Age.data,
        self.Eyes = form.Eyes.data,
        self.Hair = form.Hair.data,
        self.Height = form.Height.data


class Events(db.Model):
    __tablename__ = "events"
    event_id = db.Column("event_id", db.Integer, primary_key=True)
    Event_name = db.Column("event_name", db.String, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.now)

    user_idIdFk = db.Column("user_idIdFk", db.Integer, db.ForeignKey("users.user_id"))
    User = db.relationship("Users", backref=backref('Events', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return EventsViewModel(
            Event_name=self.Event_name,
            CreatedOn=self.CreatedOn,
            User=self.user_idIdFk
        )

    def map_from(self, form):
        self.Event_name = form.Event_name.data,
        self.user_idIdFk = form.User.data


class Options(db.Model):
    __tablename__ = "options"

    option_id = db.Column("option_id", db.Integer, primary_key=True)
    Place = db.Column("place", db.String, nullable=False)
    Season = db.Column("season", db.String, nullable=False)
    Temperature = db.Column("temperature", db.Integer, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.now)

    event_idIdFk = db.Column("event_idIdFk", db.Integer, db.ForeignKey("events.event_id"))
    Event = db.relationship("Events", backref=backref('Options', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return OptionsViewModel(
            Place=self.Place,
            Season=self.Season,
            Temperature=self.Temperature,
            CreatedOn=self.CreatedOn,
            Event=self.event_idIdFk
        )

    def map_from(self, form):
        self.Place = form.Place.data,
        self.Season = form.Season.data,
        self.Temperature = form.Temperature.data,
        self.event_idIdFk = form.Event.data


class Clothes(db.Model):
    __tablename__ = "clothes"

    clothe_id = db.Column("clothe_id", db.Integer, primary_key=True)
    Outwear = db.Column("outwear", db.String, nullable=False)
    Lowerwear = db.Column("lowerwear", db.String, nullable=False)
    Shoes = db.Column("shoes", db.Integer, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.now)

    option_idIdFk = db.Column("option_idIdFk", db.Integer, db.ForeignKey("options.option_id"))
    Option = db.relationship("Options", backref=backref('Clothes', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return ClothesViewModel(
            Outwear=self.Outwear,
            Lowerwear=self.Lowerwear,
            Shoes=self.Shoes,
            CreatedOn=self.CreatedOn,
            Option=self.option_idIdFk
        )

    def map_from(self, form):
        self.Outwear = form.Outwear.data,
        self.Lowerwear = form.Lowerwear.data,
        self.Shoes = form.Shoes.data,
        self.option_idIdFk = form.Option.data
