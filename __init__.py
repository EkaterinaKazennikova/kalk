# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'katya_secret'
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:4511@localhost:5432/kalk'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from .parameters import parameters_bp
    app.register_blueprint(parameters_bp)

    # blueprint for non-auth parts of app
    from .bmi import bmi as bmi_blueprint
    app.register_blueprint(bmi_blueprint)

    # blueprint for non-auth parts of app
    from .nutrition import nutrition as nutrition_blueprint
    app.register_blueprint(nutrition_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
