from flask import Flask, url_for, redirect, flash, Blueprint
from flask import request, render_template
from flask import session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from .models import User, Nutrition, Parameters, db

nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/nutrition')


@login_required
@nutrition_bp.route("/diary")
def nutrition_diary():
    nutrition_logs = Nutrition.query.filter_by(user_id=current_user.id)
    return render_template("nutrition_diary.html", nutrition_logs=nutrition_logs)


@login_required
@nutrition_bp.route("/create", methods=["GET", "POST"])
def nutrition_create():
    if request.method == "POST":
        nutrition_log = Nutrition(
            food=request.form["food"],
            water=request.form["water"],
            workout=request.form["workout"],
            user_id=current_user.id
        )
        db.session.add(nutrition_log)
        db.session.commit()
        flash("Вы успешно внесли свои данные")
    return render_template("nutrition_form.html")
