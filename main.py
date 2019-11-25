import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from dao.orm.entities import *
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
import json
from sqlalchemy import func
from dao.db import PostgresDb
from forms.forms import *

app = Flask(__name__)
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:134951m@localhost/receipt_webservice'
app.debug = True
db = PostgresDb()

@app.route('/')
def index():
    return render_template('index.html')
#RESTAURANT
@app.route('/get', methods = ['GET'])
def index_get():
    allRestaurants = db.sqlalchemy_session.query(Restaurant).all()
    return render_template('restaurant.html', allRestaurants = allRestaurants)

@app.route('/new_restaurant', methods=['GET', 'POST'])
def new_restaurant():
    form = RestorauntForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('restaurant_form.html', form=form, form_name="New restaurant", action="new_restaurant")
        else:
            restaurant_obj = Restaurant(
                name=form.name.data,
                dishname_fk=form.dishname_fk.data,
                star=form.star.data,
                country=form.country.data,
                city=form.city.data,
                address=form.address.data
            )
            print(restaurant_obj)
            a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.dishname_fk.data).all()
            if not a:
                return render_template('restaurant_form.html', form=form, form_name="New restaurant",
                                       action="new_restaurant")
            db.sqlalchemy_session.add(restaurant_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_get'))

    return render_template('restaurant_form.html', form=form, form_name="New restaurant", action="new_restaurant")


@app.route('/edit_restaurant', methods=['GET', 'POST'])
def edit_restaurant():
    db = PostgresDb()
    form = RestorauntForm()
    if request.method == 'GET':

        restaurantname = request.args.get('name')
        db = PostgresDb()

        restaurant_obj = db.sqlalchemy_session.query(Restaurant).filter(Restaurant.name == restaurantname).one()

        form.name.data = restaurant_obj.name,
        form.dishname_fk.data = restaurant_obj.dishname_fk
        form.star.data = restaurant_obj.star
        form.country.data = restaurant_obj.country
        form.city.data = restaurant_obj.city
        form.address.data = restaurant_obj.address


        form.old_name.data = restaurant_obj.name

        return render_template('restaurant_form.html', form=form, form_name="Edit restaurant", action="edit_restaurant")

    else:
        if not form.validate():
            return render_template('restaurant_form.html', form=form, form_name="Edit restaurant",
                                   action="edit_restaurant")
        else:
            restaurant_obj = db.sqlalchemy_session.query(Restaurant).filter(Restaurant.name == form.old_name.data).one()


            restaurant_obj.city = form.city.data
            restaurant_obj.star = form.star.data
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_get'))

@app.route('/graphics', methods=['GET'])
def graphics():
    allRestaurants = db.sqlalchemy_session.query(Restaurant).order_by(Restaurant.star)
    stars = [restaurant.star for restaurant in allRestaurants]
    bar = go.Bar(
        x=stars,
        y=[restaurant.star for restaurant in allRestaurants]
    )
    ids=[1]
    data = [bar]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graphics.html', graphJSON=graphJSON, ids=ids)


    data = [bar]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
# TYPE
@app.route('/type', methods = ['GET'])
def index_type():
    myType = db.sqlalchemy_session.query(Type).all()

    return render_template('type.html', allTypes = myType)

@app.route('/new_type', methods=['GET', 'POST'])
def new_type():
    form = TypeForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('type_form.html', form=form, form_name="New type", action="new_type")
        else:
            q = db.sqlalchemy_session.query(func.max(Type.id)).one()
            list_of_max = list(q)
            new_index = list_of_max[0] + 1
            type_obj = Type(
                id=new_index,
                typename=form.typename.data,
                dishname_fk=form.dishname_fk.data
            )
            a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.dishname_fk.data).all()
            if not a:
                return render_template('type_form.html', form=form, form_name="New type",
                                       action="new_type")
            db.sqlalchemy_session.add(type_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_type'))

    return render_template('type_form.html', form=form, form_name="New type", action="new_type")


@app.route('/edit_type', methods=['GET', 'POST'])
def edit_type():
    db = PostgresDb()
    form = TypeForm()
    if request.method == 'GET':

        typeid = request.args.get('name')
        db = PostgresDb()

        typeobj = db.sqlalchemy_session.query(Type).filter(Type.id == typeid).one()

        form.typename.data = typeobj.typename
        form.dishname_fk.data = typeobj.dishname_fk
        form.old_id.data = typeobj.id
        form.old_name.data = typeobj.dishname_fk
        print('type', typeobj.id)
        print('form', form.old_id.data)
        return render_template('type_form.html', form=form, form_name="Edit type", action="edit_type")

    else:
        if not form.validate():
            return render_template('type_form.html', form=form, form_name="Edit type",
                                   action="edit_type")
        else:
            typeid = request.args.get('name')
            db = PostgresDb()

            typeobj = db.sqlalchemy_session.query(Type).filter(Type.id == form.old_id.data).one()

            typeobj.typename = form.typename.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_type'))


@app.route('/delete_type')
def delete_type():
    typeid = request.args.get('name')
    db = PostgresDb()
    result = db.sqlalchemy_session.query(Type).filter(Type.id == typeid).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_type'))

@app.route('/dish', methods = ['GET'])
def index_dish():
    myDish = db.sqlalchemy_session.query(Dish).all()
    return render_template('dish.html', allDishes=myDish)


@app.route('/new_dish', methods=['GET', 'POST'])
def new_dish():
    form = DishForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('dish_form.html', form=form, form_name="New dish",
                                   action="new_dish")
        else:
            dish_obj = Dish(
                dishname=form.dishname.data,
                calories_amount = form.calories_amount.data
            )
            print(dish_obj)
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.dishname.data).all()
            if not a:
                db.sqlalchemy_session.add(dish_obj)
                db.sqlalchemy_session.commit()
                return redirect(url_for('index_dish'))
            return redirect(url_for('index_dish'))
    return render_template('dish_form.html', form=form, form_name="New dish", action="new_dish")


@app.route('/edit_dish', methods=['GET', 'POST'])
def edit_dish():
    form = DishForm()
    if request.method == 'GET':
        dishname = request.args.get('name')
        dish = db.sqlalchemy_session.query(Dish).filter(
            Dish.dishname == dishname).one()
        a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == dish.dishname).all()
        if not a:
            return render_template('dish_form.html', form=form, form_name="Edit dish",
                                   action="edit_dish")
        form.calories_amount.data = dish.calories_amount
        form.dishname.data = dish.dishname
        form.old_name.data = dish.dishname
        return render_template('dish_form.html', form=form, form_name="Edit dish", action="edit_dish")

    else:
        if not form.validate():
            return render_template('dish_form.html', form=form, form_name="Edit dish",
                                   action="edit_dish")
        else:
            dish = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.old_name.data,).one()
            dish.dishname = form.dishname.data
            dish.calories_amount = form.calories_amount.data
            db.sqlalchemy_session.commit()
            return redirect(url_for('index_dish'))


@app.route('/delete_dish')
def delete_dish():
    dishname = request.args.get('name')
    dish = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == dishname).first()
    db.sqlalchemy_session.delete(dish)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_dish'))

# RECEIPT STARTS
@app.route('/receipt')
def index_receipt():
    myReceipt = db.sqlalchemy_session.query(Receipt).all()
    return render_template('receipt.html', allReceipts = myReceipt)

@app.route('/new_receipt', methods=['GET', 'POST'])
def new_receipt():
    form = ReceiptForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('receipt_form.html', form=form, form_name="New receipt",
                                   action="new_receipt")
        else:
            receipt_obj = Receipt(
                dishname_fk=form.dishname_fk.data,
                receipt_content=form.receipt_content.data
            )
            db = PostgresDb()

            a = db.sqlalchemy_session.query(Dish).filter(Dish.dishname == form.dishname_fk.data).all()
            if not a:
                return render_template('receipt_form.html', form=form, form_name="New receipt",
                                       action="new_receipt")
            db.sqlalchemy_session.add(receipt_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_receipt'))

    return render_template('receipt_form.html', form=form, form_name="New receipt", action="new_receipt")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    dishes = db.sqlalchemy_session.query(Dish).order_by(Dish.calories_amount)
    calories = [dish.calories_amount for dish in dishes]
    bar = go.Bar(
        x=calories,
        y=[dish.dishname for dish in dishes]
    )

    names = set()
    for type_e in db.sqlalchemy_session.query(Type).distinct():
        names.add(type_e.typename)
        print("type names", type_e.typename)

    values = []
    for i in names:
        q = db.sqlalchemy_session.query(func.count(Type.typename)).filter(Type.typename == i).one()
        list_of_max = list(q)
        new_index = list_of_max[0]
        values.append(new_index)

    names_converted = tuple(names)

    scatter = go.Scatter(
        x=names_converted,
        y=values,
    )
    print(scatter)
    ids = [0, 1]
    data = [bar, scatter]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    #bar_data = [bar]
    #graphJSON1 = json.dumps(bar_data, cls=plotly.utils.PlotlyJSONEncoder)


    # names = set()
    # for type_e in db.sqlalchemy_session.query(Type).distinct():
    #     names.add(type_e.typename)
    #     print("type names", type_e.typename)
    # values = []
    #
    # for i in names:
    #     q = db.sqlalchemy_session.query(func.count(Type.typename)).filter(Type.typename == i).one()
    #     list_of_max = list(q)
    #     new_index = list_of_max[0]
    #     print("new index", new_index)
    # names_converted = tuple(names)
    # pie = go.Pie(labels=names_converted, values=values)
    # pie_data = [pie]
    #
    # graphJSON2 = json.dumps(pie_data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphJSON=graphJSON, ids=ids)
   # return render_template('dashboard.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2, ids=ids)

# @app.route('/edit_receipt', methods=['GET', 'POST'])
# def edit_receipt():
#     form = ReceiptForm()
#     dish = request.args.get('name')
#
#     if request.method == 'GET':
#         print(dish)
#     else:
#         print(dish)
#     #     #
#     #     dish = db.session.query(Receipt).filter(
#     #         Receipt.dish == dish).one()
#     #     print(dish)
#     #     a = db.session.query(Receipt).filter(Receipt.dish == Receipt.dish).all()
#     #     if not a:
#     #         return render_template('receipt_form.html', form=form, form_name="Edit receipt",
#     #                                action="edit_receipt")
#     #     form.receipt.data = dish.receipt
#     #     form.dish.data = dish.dish
#     #     form.old_name.data = dish.dish
#     #     return render_template('receipt_form.html', form=form, form_name="Edit receipt", action="edit_receipt")
#     #
#     # else:
#     #     if not form.validate():
#     #         return render_template('receipt_form.html', form=form, form_name="Edit receipt",
#     #                                action="edit_receipt")
#     #     else:
#     #         dish = db.session.query(Receipt).filter(Receipt.dish == form.old_name.data,).one()
#     #         dish.dish = form.dish.data
#     #         dish.receipt = form.receipt.data
#     #         db.session.commit()
#         return redirect(url_for('index_receipt'))
#
# @app.route('/delete_receipt')
# def delete_receipt():
#
#     dishreceipt = request.args.get('name')
#     dish = db.sqlalchemy_session.query(Receipt).filter(Receipt.dish == dishreceipt).first()
#     # result = db.query(Receipt).filter(
#     #     Receipt.dish == dishreceipt).one()
#
#     db.sqlalchemy_session.delete(dish)
#     db.sqlalchemy_session.commit()
#     #
#     return redirect(url_for('index_receipt'))
#
# @app.route('/ingridients')
# def index_ingridient():
#     myIngridient = db.sqlalchemy_session.query(Ingridients).all()
#     return render_template('ingridients.html', allIngridients = myIngridient)
#
# @app.route('/new_ingridient', methods=['GET', 'POST'])
#
# @app.route('/edit_ingridient', methods=['GET', 'POST'])
# def edit_ingridient():
#     form = IngridientForm()
#     if request.method == 'GET':
#         dish = request.args.get('name')
#         #
#         dish = db.session.query(Ingridients).filter(
#             Ingridients.dishname == dish).one()
#         a = db.session.query(Ingridients).filter(Ingridients.dishname == Ingridients.dishname).all()
#         print(a)
#         if not a:
#             return render_template('ingridients_form.html', form=form, form_name="Edit ingridient",
#                                    action="edit_ingridient")
#         form.dishname.data = dish.dishname
#         form.ingridients.data = dish.ingridients
#         form.old_name.data = dish.dishname
#         return render_template('ingridients_form.html', form=form, form_name="Edit ingridient", action="edit_ingridient")
#
#     else:
#         if not form.validate():
#             return render_template('ingridients_form.html', form=form, form_name="Edit ingridient",
#                                    action="edit_ingridient")
#         else:
#             dish = db.session.query(Ingridients).filter(Ingridients.dishname == form.old_name.data, ).one()
#             dish.ingridients = form.ingridients.data
#             db.session.commit()
#             return redirect(url_for('index_ingridient'))

#
# def new_ingridient():
#     form = IngridientForm()
#     if request.method == 'POST':
#         if not form.validate():
#             return render_template('ingridients_form.html', form=form, form_name="New ingridient",
#                                    action="new_ingridient")
#         else:
#             ingridients_obj = Ingridients(
#                 ingridientname=form.ingridientname.data)
#             db = PostgresDb()
#             a = db.sqlalchemy_session.query(Ingridients).filter(Ingridients.ingridientname == form.ingridientname.data).all()
#             if not a:
#                 return render_template('ingridients_form.html', form=form, form_name="New ingridient",
#                                        action="new_ingridient")
#
#             db.sqlalchemy_session.add(ingridients_obj)
#             db.sqlalchemy_session.commit()
#
#             return redirect(url_for('index_ingridient'))
#
#     return render_template('ingridients_form.html', form=form, form_name="New ingridient", action="new_ingridient")
#
if __name__ == "__main__":
    app.run()