# init.py

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'katya_secret'
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:4511@localhost:5432/kalk'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     # since the user_id is just the primary key of our user table, use it in the query for the user
    #     with app.app_context():
    #         user = User.query.get(int(user_id))
    #         return user

    # blueprint for auth routes in our app


    return app

#
# if __name__ == "__main__":
#     app = create_app()
#     app.run()
