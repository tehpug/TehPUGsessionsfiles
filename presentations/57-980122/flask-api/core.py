import os

from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Foods(db.Model):
    __name__ = "foods"

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer)
    food_type = db.Column(db.String(12))
    food_name =  db.Column(db.Text)
    food_image= db.Column(db.Text)
    food_url  = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    recipe = db.Column(db.Text)


def make_all(data):
    return data.all()

def make_paginate(data, page, weight):
    return data.paginate(page, weight, False)


@app.route("/main_course/")
@app.route("/main_course/<int:page>/")
@app.route("/main_course/<int:page>/<int:weight>")
def index(page=1, weight=20):
    foods = Foods.query.filter(Foods.food_type=="main_course").paginate(page, weight, False)
    result = list()
    for food in foods.items:
        obj = dict()
        obj['id'] = food.id
        obj['food_id'] = food.food_id
        obj['food_type'] = food.food_type
        obj['food_name'] = food.food_name
        obj['food_image'] = food.food_image
        obj['ingredients'] = food.ingredients
        obj['recipe'] = food.recipe
        result.append(obj)

    return jsonify({"result": result})


@app.route("/main_course/random/")
def random_food():
    food = Foods.query.filter_by(food_type="main_course").order_by(func.random()).first()

    obj = dict()
    obj['id'] = food.id
    obj['food_id'] = food.food_id
    obj['food_type'] = food.food_type
    obj['food_name'] = food.food_name
    obj['food_image'] = food.food_image
    obj['ingredients'] = food.ingredients
    obj['recipe'] = food.recipe
    return jsonify({"result": obj})
