from flask import Flask, url_for, redirect, flash, Blueprint
from flask import request, render_template
from flask import session
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re

from models import User, Nutrition, Parameters, db

parameters_bp = Blueprint('parameters', __name__, url_prefix='/parameters')


@parameters_bp.route("/")
@login_required
def parameters():
    params = Parameters.query.filter_by(user_id=current_user.id).order_by(desc(Parameters.id))
    return render_template("parameters.html", user=current_user.name, params=params)


@parameters_bp.route("/create", methods=["GET", "POST"])
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
        return redirect(url_for('.parameters'))
    return render_template("parameters_form.html")


@parameters_bp.route("/update", methods=["GET", "POST"])
@login_required
def parameters_update():
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
        flash("Ваши данные успешно обновлены")
        return redirect(url_for('.parameters'))
    return render_template("parameters_form.html")