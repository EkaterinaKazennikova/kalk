# main.py

from flask import Blueprint, render_template, Flask, url_for, current_app, redirect
from flask_login import login_required, current_user, login_manager
from flask_sqlalchemy import SQLAlchemy

from app import create_app, login_manager
from models import User

index_bp = Blueprint('index', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()


@index_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('index.data'))
    return redirect(url_for('auth.login'))


@index_bp.route('/data')
def data():
    return render_template('data.html', name=current_user.name)



from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(index_bp)

# blueprint for non-auth parts of app
from parameters import parameters_bp
app.register_blueprint(parameters_bp)

# blueprint for non-auth parts of app
from bmi import bmi_bp
app.register_blueprint(bmi_bp)

# blueprint for non-auth parts of app
from nutrition import nutrition_bp
app.register_blueprint(nutrition_bp)


if __name__ == "__main__":
    app.run(debug=True)
