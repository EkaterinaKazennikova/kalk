from flask import Flask, url_for, redirect, flash, Blueprint
from flask import request, render_template
from flask import session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from .models import User, Nutrition, Parameters, db

bmi = Blueprint('bmi', __name__)


@bmi.route("/")
def get_bmi():
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
