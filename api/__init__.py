# Naming the file __init__.py makes this directory ("website") a python package, meaning that when this directory is imported into another python file, __init__.py will run.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    # This creates the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'randomstring'

    # This tells the app where to find the database
    # The database file will be stoted in the local directory
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # This tells the app where to find the routes
    from .views import views_blueprint
    from .auth import auth_blueprint

    app.register_blueprint(views_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/')
    # If url_prefix was '/auth/' and the route stored in auth.py was 'login'
    # then the route would be '/auth/login'

    from .models import User, Note
    # This will run the models.py file, and create the models

    with app.app_context():
        db.create_all()
        print('Created Database!')

    login_manager = LoginManager()
    login_manager.login_view = 'auth_str.login'
    # This is where the user is redirected if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app