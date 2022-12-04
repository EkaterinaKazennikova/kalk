from flask import Flask, url_for, redirect, flash, Blueprint
from flask import request, render_template
from flask import session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from .models import User, Nutrition, Parameters, db

nutrition = Blueprint('nutrition', __name__)


@nutrition.route("/create", methods=["GET", "POST"])
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
