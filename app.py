from flask import Flask, request, render_template, redirect, url_for
from domain.models import db, Users, Events, Options, Clothes
from domain.credentials import *
from views.users import UsersViewModel
from views.events import EventsViewModel
from views.options import OptionsViewModel
from views.clothes import ClothesViewModel
from views.dashboard import DashboardViewModel
from services.visualization import user_distribution_pie, event_options_population_bar
from sqlalchemy import desc
import os

app = Flask(__name__)
app.secret_key = 'development key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


@app.route("/")
def index():
    db.create_all()
    return render_template("layout.html")


@app.route("/users")
def users():
    all_users = Users.query.all()
    return render_template("users/index.html", users=all_users)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    form = UsersViewModel()

    if request.method == "POST":
        if not form.validate():
            return render_template("users/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("users"))

    return render_template("users/create.html", form=form)


@app.route("/users/delete/<uuid>", methods=["POST"])
def delete_user(uuid):
    user = Users.query.filter(Users.user_id == uuid).first()
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("users"))


@app.route("/users/<uuid>", methods=["GET", "POST"])
def update_user(uuid):
    user = Users.query.filter(Users.user_id == uuid).first()
    form = user.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("users/update.html", form=form)

        user.map_from(form)
        db.session.commit()
        return redirect(url_for("users"))

    return render_template("users/update.html", form=form)

@app.route("/events")
def events():
    all_events = Events.query.join(Users).order_by(desc(Events.CreatedOn)).all()
    return render_template("events/index.html", events=all_events)


@app.route("/events/new", methods=["GET", "POST"])
def new_event():
    form = EventsViewModel()
    form.User.choices = [(str(user.user_id), user.Login) for user in Users.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("events/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("events"))

    return render_template("events/create.html", form=form)


@app.route("/events/delete/<uuid>", methods=["POST"])
def delete_event(uuid):
    event = Events.query.filter(Events.event_id == uuid).first()
    if event:
        db.session.delete(event)
        db.session.commit()

    return redirect(url_for("events"))


@app.route("/events/<uuid>", methods=["GET", "POST"])
def update_event(uuid):
    event = Events.query.filter(Events.event_id == uuid).first()
    form = event.wtf()
    form.User.choices = [(str(user.user_id), user.Login) for user in Users.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("events/update.html", form=form)
        event.map_from(form)
        db.session.commit()
        return redirect(url_for("events"))

    return render_template("events/update.html", form=form)

@app.route("/options")
def options():
    all_options = Options.query.join(Events).order_by(desc(Options.CreatedOn)).all()
    return render_template("options/index.html", options=all_options)


@app.route("/options/new", methods=["GET", "POST"])
def new_option():
    form = OptionsViewModel()
    form.Event.choices = [(str(event.event_id), event.Event_name) for event in Events.query.join(Users, Events.user_idIdFk == Users.user_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("options/create.html", form=form)
        else:
            user = form.domain()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("options"))

    return render_template("options/create.html", form=form)


@app.route("/options/<uuid>", methods=["GET", "POST"])
def update_option(uuid):
    option = Options.query.filter(Options.option_id == uuid).first()
    form = option.wtf()
    form.Event.choices = [(str(event.event_id), event.Event_name) for event in
                          Events.query.join(Users, Events.user_idIdFk == Users.user_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("options/update.html", form=form)
        option.map_from(form)
        db.session.commit()
        return redirect(url_for("options"))

    return render_template("options/update.html", form=form)


@app.route("/options/delete/<uuid>", methods=["POST"])
def delete_option(uuid):
    option = Options.query.filter(Options.option_id == uuid).first()
    if option:
        db.session.delete(option)
        db.session.commit()

    return redirect(url_for("options"))

@app.route("/clothes")
def clothes():
    all_clothes = Clothes.query.join(Options).all()
    return render_template("clothes/index.html", clothes=all_clothes)


@app.route("/clothes/new", methods=["GET", "POST"])
def new_clothe():
    form = ClothesViewModel()
    form.Option.choices = [(str(option.option_id), option.Place) for option
                           in Options.query.join(Events, Options.event_idIdFk == Events.event_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("clothes/create.html", form=form)
        else:
            event = form.domain()
            db.session.add(event)
            db.session.commit()
            return redirect(url_for("clothes"))

    return render_template("clothes/create.html", form=form)


@app.route("/clothes/<uuid>", methods=["GET", "POST"])
def update_clothe(uuid):
    clothe = Clothes.query.filter(Clothes.clothe_id == uuid).first()
    form = clothe.wtf()
    form.Option.choices = [(str(option.option_id), option.Place) for option
                           in Options.query.join(Events, Options.event_idIdFk == Events.event_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("clothes/update.html", form=form)
        clothe.map_from(form)
        db.session.commit()
        return redirect(url_for("clothes"))

    return render_template("clothes/update.html", form=form)


@app.route("/clothes/delete/<uuid>", methods=["POST"])
def delete_clothe(uuid):
    clothe = Clothes.query.filter(Clothes.clothe_id == uuid).first()
    if clothe:
        db.session.delete(clothe)
        db.session.commit()

    return redirect(url_for("clothes"))

@app.route("/dashboard")
def dashboard():
    all_users = db.session.query(Users.user_id, Users.Login).all()
    distinct_events = db.session.query(Events.Event_name).distinct().all()
    dashboardViewModel = DashboardViewModel()
    if len(all_users):
        dashboardViewModel.Users = [(str(user.user_id), user.Login) for user in all_users]
        dashboardViewModel.Users_distribution_data = user_distribution_pie(all_users[0][0])

    if len(distinct_events):
        dashboardViewModel.Events = distinct_events
        dashboardViewModel.Events_options_population_data = event_options_population_bar(
            distinct_events[0][0])

    return render_template("dashboard/index.html", model=dashboardViewModel)


@app.route("/user_distribution/<uuid>")
def user_distribution(uuid):
    return user_distribution_pie(uuid)


@app.route("/event_options_population/<name>")
def event_options_population(name):
    return event_options_population_bar(name)


if __name__ == "__main__":
    app.run(debug=True)
