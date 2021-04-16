from flask import Flask, render_template, request, redirect, url_for

from dao.orm.entities import *
from datetime import date
import json as json
from dao.db import PostgresDb
from forms.forms import *

import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.secret_key = 'development key'
app.debug = True
db = PostgresDb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods = ['GET'])
def index_user():
    allUsers = db.sqlalchemy_session.query(User).all()
    return render_template('user.html', allUsers = allUsers)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('user_form.html', form=form, form_name="New user",
                                   action="new_user")
        else:
            user_obj = User(
                Username=form.Username.data,
                Password = form.Password.data,
                Company = form.Company.data

            )
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Company).filter(Company.Company == form.Company.data).all()
            b = db.sqlalchemy_session.query(User).filter(User.Username == form.Username.data).all()

            if not a:
                return redirect(url_for('index_user'))
            if b:
                return redirect(url_for('index_user'))

            db.sqlalchemy_session.add(user_obj)
            db.sqlalchemy_session.commit()

    return render_template('user_form.html', form=form, form_name="New user", action="new_user")
@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form = UserForm()
    if request.method == 'GET':
        name = request.args.get('name')
        db = PostgresDb()
        user = db.sqlalchemy_session.query(User).filter(
        User.Username == name).one()

        a = db.sqlalchemy_session.query(Company).filter(Company.Company == user.Company).all()

        if not a:
            return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")

        form.Username.data = user.Username
        form.Password.data = user.Password
        form.Company.data = user.Company
        form.old_name.data = user.Username
        return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")
        
    else:

        if not form.validate():
            return render_template('user_form.html', form=form, form_name="Edit user",
                                    action="edit_user")
        else:
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Company).filter(Company.Company == form.Company.data).all()

            if not a:
                return render_template('user_form.html', form=form, form_name="Edit user",
                                    action="edit_user")

            user = db.sqlalchemy_session.query(User).filter(User.Username == form.old_name.data ).one()
    
            user.Username = form.Username.data
            user.Password = form.Password.data
            user.Company = form.Company.data
            

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_user'))
    
@app.route('/delete_user')
def delete_user():
    allUsers = db.sqlalchemy_session.query(User).all()

    name = request.args.get('name')
    thisUser = db.sqlalchemy_session.query(User).filter(User.Username == name).first()
   
    db.sqlalchemy_session.delete(thisUser)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_user'))

@app.route('/messages', methods = ['GET'])
def index_message():
    allMesages = db.sqlalchemy_session.query(Message).all()
    return render_template('messages.html', allMesages = allMesages)

@app.route('/new_message', methods=['GET', 'POST'])
def new_message():
    db = PostgresDb()
    form = MessagesForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('message_form.html', form=form, form_name="New message", action="new_message")
        else:
            message_obj = Message(
                MessageSender=form.MessageSender.data,
                MessageContent = form.MessageContent.data,
                MessageDate = date.today()
            )
            print(message_obj)
            a = db.sqlalchemy_session.query(User).filter(User.Username == form.MessageSender.data).all()
            # b = db.sqlalchemy_session.query(User).filter(User.Username == form.Username.data).all()

            if not a:
                return redirect(url_for('index_message'))
            # if b:
            #     return redirect(url_for('index_user'))

            db.sqlalchemy_session.add(message_obj)
            db.sqlalchemy_session.commit()
            return redirect(url_for('index_message'))


    return render_template('message_form.html', form=form, form_name="New message", action="new_message")

@app.route('/edit_message', methods=['GET', 'POST'])

def edit_message():
    form = MessagesForm()
    db = PostgresDb()
    if request.method == 'GET':
        message_id = request.args.get('name')
        message = db.sqlalchemy_session.query(Message).filter(Message.MessageID == message_id).one()

        a = db.sqlalchemy_session.query(Message).filter(Message.MessageID == message.MessageID).all()

        if not a:
            return render_template('message_form.html', form=form, form_name="Edit message", action="edit_message")
        print(message.MessageSender)
        print(message.MessageContent)
        form.MessageSender.data = message.MessageSender
        form.MessageContent.data = message.MessageContent
        form.old_name.data = message.MessageID
        return render_template('message_form.html', form=form, form_name="Edit message", action="edit_message")
        
    else:
        if not form.validate():
            print('form is not validate qwhy')
            print()
            return render_template('message_form.html', form=form, form_name="Edit message",
                                    action="edit_message")
        else:
            print('IM HEREEE')
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Message).filter(Message.MessageID == form.old_name.data).all()

            if not a:
                return render_template('message_form.html', form=form, form_name="Edit message",
                                    action="edit_message")
            print('IM HERE TOOOO')
            message = db.sqlalchemy_session.query(Message).filter(Message.MessageID == form.old_name.data ).one()
    
            message.MessageContent = form.MessageContent.data
            

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_message'))
   
@app.route('/delete_message')
def delete_message():
    allMesages = db.sqlalchemy_session.query(User).all()

    message_id = request.args.get('name')
    thisMessage = db.sqlalchemy_session.query(allMesages).filter(Message.MessageID == message_id).first()
   
    db.sqlalchemy_session.delete(thisMessage)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_message'))

@app.route('/company', methods = ['GET'])
def index_company():
    allCompanies = db.sqlalchemy_session.query(Company).all()
    return render_template('companies.html', allCompanies = allCompanies)

@app.route('/new_company', methods=['GET', 'POST'])
def new_company():
    form = CompaniesForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('companies_form.html', form=form, form_name="New company", action="new_company")
        else:
            company_obj = Company(
                 Company=form.Company.data,
            )
            db.sqlalchemy_session.add(company_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_company'))

    return render_template('companies_form.html', form=form, form_name="New company", action="new_company")

@app.route('/edit_company', methods = ['GET'])
def edit_company():
    form = CompaniesForm()

    if request.method == 'GET':

        company = request.args.get('name')
        db = PostgresDb()
        companyobj = db.sqlalchemy_session.query(Company).filter(Company.Company == company).one()

        form.Company.data = companyobj.Company
        form.old_name.data = companyobj.Company
        return render_template('companies_form.html', form=form, form_name="Edit company", action="new_company")

    else:
        if not form.validate():
            return render_template('companies_form.html', form=form, form_name="Edit company",
                                    action="edit_company")
        else:
            db = PostgresDb()

            companyobj = db.sqlalchemy_session.query(Company).filter(Company.Company == form.old_name.data).one()
            companyobj.Company = form.Company.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_company'))

@app.route('/delete_company')
def delete_company():
    allCompanies = db.sqlalchemy_session.query(Company).all()

    name = request.args.get('name')
    thisCompany = db.sqlalchemy_session.query(Company).filter(Company.Company == name).first()
   
    db.sqlalchemy_session.delete(thisCompany)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_company'))


@app.route('/dashboard')
def dashboard_def():

    names = set()
    for numes in db.sqlalchemy_session.query(Message.MessageSender).distinct():
        names.add(numes.MessageSender)
        print("type names", numes.MessageSender)
    names_converted = tuple(names)

    values = []
    for i in names:
        q = db.sqlalchemy_session.query(func.count(Message.MessageSender)).filter(Message.MessageSender == i).one()
        list_of_max = list(q)
        new_index = list_of_max[0]
        values.append(new_index)

    bar = go.Bar(
        x=names_converted,
        y=values,
    )
    scatter = go.Scatter(
        x=names_converted,
        y=values,
    )
    
    # messages = db.sqlalchemy_session.query(Message).order_by(Message.MessageContent)
    # calories = [dish.calories_amount for dish in messages]
    # bar = go.Bar(
    #     x=calories,
    #     y=[dish.dishname for dish in messages]
    # )
    
    # scatter = go.Scatter(
    #     x=calories,
    #     y=[dish.dishname for dish in messages],
    # )
    ids = [0, 1]
    data =[scatter, bar]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphJSON=graphJSON, ids=ids)


@app.route('/shop', methods = ['GET'])
def index_shop():
    messenger_data = db.sqlalchemy_session.query(Messenger).all()
    print(messenger_data)
    return render_template('messenger.html', messengers_data = messenger_data)


@app.route('/insert', methods=['GET', 'POST'])
def new_messenger():
    form = MessengerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('insertion.html', form=form, form_name="", action="insert")
        else:
            msg_data = Messenger(
                Site = form.Site.data,
                Version = form.Version.data,
                Country = form.Country.data,
                Price = form.Price.data,
                Username =form.Username.data
            )
            db.sqlalchemy_session.add(msg_data)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_shop'))

    return render_template('insertion.html', form=form, form_name="New messenger", action="insert")


@app.route('/plotly')
def draw_plot():
    messenger_names = set()
    for numes in db.sqlalchemy_session.query(Messenger.Site).distinct():
        messenger_names.add(numes.Site)
        print("type names", numes.Site)
    names_converted = tuple(messenger_names)

    prices = []
    for i in messenger_names:
        query_data = db.sqlalchemy_session.query(Messenger.Price).filter(Messenger.Site == i).one()
        print('query data', query_data)
        list_form_of_query_response = list(query_data)
        print('list_form_of_query_response', list_form_of_query_response)

        new_index = list_form_of_query_response[0]
        prices.append(new_index)

    print(prices)
    pie_data = go.Pie(
        labels=names_converted,
        values=prices,
    )

    ids = [0]
    data =[pie_data]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphJSON=graphJSON, ids=ids)
    

if __name__ == "__main__":
    app.run()