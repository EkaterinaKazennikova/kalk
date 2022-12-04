from flask import Flask, url_for, redirect, flash, Blueprint
from flask import request, render_template
from flask import session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from .models import User, Nutrition, Parameters, db

parameters = Blueprint('parameters', __name__, url_prefix='/parameters')


@parameters.route("/create", methods=["GET", "POST"])
@login_required
def parameters_create():
    if request.method == "POST":
        params = Parameters(
            age=request.form["age"],
            gender=request.form["gender"],
            weight=request.form["weight"],
            height=request.form["height"],
            user_id=current_user.id
        )
        db.session.add(params)
        db.session.commit()
        flash("Ваши данные успешно внесены")
        return redirect(url_for('main.index'))
    return render_template("parameters.html")