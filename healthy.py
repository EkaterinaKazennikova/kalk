from flask import Flask, url_for, redirect, flash
from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.secret_key = 'secret'
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:4511@localhost:5432'
db.init_app(app)


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    parameters = db.relationship('Parameters', back_populates='account')


class Parameters(db.Model):
    __tablename__ = "parameters"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, ForeignKey("account.id"))
    account = db.relationship('Account', back_populates='parameters')


class Nutrition(db.Model):
    __tablename__ = "nutrition"
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String, unique=True, nullable=False)
    water = db.Column(db.Integer, nullable=False)
    workout = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

'''Валидация формата пароля'''


class ValidationError(Exception):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

    def validate_by_regexp(self, password, pattern):
        if re.match(pattern, password) is None:
            raise ValidationError('Введите пароль,содержащий не менее 8 символов в обоих регистрах')


@app.route("/")
def Head():
    return render_template("index.html", title="Healthy Nutrition")


@app.route("/account/create", methods=["GET", "POST"])
def account_create():
    if request.method == "POST":
        hashAndSalt = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())
        account = Account(
            login=request.form["login"],
            password=hashAndSalt,
            email=request.form["email"],
        )
        db.session.add(account)
        db.session.commit()
        flash("Вы успешно зарегистрированы")
        return render_template("success.html")

    return render_template("account.html")


@app.route("/parameters/create", methods=["GET", "POST"])
def parameters_create():
    if request.method == "POST":
        parameters = Parameters(
            username=request.form["username"],
            age=request.form["age"],
            gender=request.form["gender"],
            weight=request.form["weight"],
            height=request.form["height"]
        )
        db.session.add(parameters)
        db.session.commit()
        flash("Ваши данные успешно внесены")
        return render_template("success.html")
    return render_template("parameters.html")

@app.route("/bmi/create", methods=["GET", "POST"])
def bmi_get():
    if request.method == "GET":
        weight = request.args.get["weight"]
        height = request.args.get["height"]
        bmi = weight / (height ** 2)
        return f'''Ваш индекс массы тела, {bmi}'''

        #if request.form.gender == 'female':
            #flash('Ваше рекомендуемое количесво каллорий в день')
            #return render_template("female.html")
        #else:
        #flash('Ваше рекомендуемое количесво каллорий в день')
        #return render_template("male.html")
        #return redirect(url_for("parameters_detail", id=parameters.id))


    #, lambda weight, height, age: 88 + weight * 14 + height * 5 - 6 * age)
         #flash('Ваше рекомендуемое количесво каллорий в день', lambda weight, height, age: 447 + weight * 9 + height * 3 - 4 * age)

@app.route("/nutrition/create", methods=["GET", "POST"])
def nutrition_create():
    if request.method == "POST":
        nutrition = Nutrition(
            food=request.form["food"],
            water=request.form["water"],
            workout=request.form["workout"],
        )
        db.session.add(nutrition)
        db.session.commit()
        flash("Вы успешно внесли свои данные")
        return render_template("success.html")

    return render_template("nutrition.html")


if __name__ == "__main__":
    app.run(debug=True)
