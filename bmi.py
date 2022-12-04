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

bmi_bp = Blueprint('bmi', __name__, url_prefix='/bmi')


@login_required
@bmi_bp.route("/")
def bmi():
    params = Parameters.query.filter_by(user_id=current_user.id).order_by(desc(Parameters.id)).first()
    if params:
        bmi = calculate_bmi(
            params.weight,
            params.height,
            params.gender,
            params.age
        )
        return render_template("bmi.html", bmi=bmi)
    return render_template("bmi_none.html")


def calculate_bmi(weight, height, gender, age):
    if gender == 'male':
        return 88 + weight * 14 + height * 5 - 6 * age
    if gender == 'female':
        return 447 + weight * 9 + height * 3 - 4 * age
