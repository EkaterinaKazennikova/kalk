# main.py

from flask import Blueprint, render_template, Flask, url_for, current_app, redirect
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy

main = Blueprint('main', __name__)


app = Flask(__name__)
app.secret_key = 'secret'
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:4511@localhost:5432/kalk'
db.init_app(app)

with app.app_context():
    db.create_all()


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return redirect(url_for('login'))


@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)
