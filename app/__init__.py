from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite'
    app.config['SECRET_KEY'] = 'jkg43guign83n4y898n98y98N878788886ggHSDL8D894,S'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(app)

    from .models import Users
    @login_manager.user_loader
    def load_user(user_id):
        user = Users.query.get(int(user_id))
        return user

    from .routers import main, task, auth
    app.register_blueprint(main.main)
    app.register_blueprint(task.task)
    app.register_blueprint(auth.auth)


    return app
