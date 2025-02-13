from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login  import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sayedmuhammadidrees'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{ path.abspath('website/' + DB_NAME)}"  
   
    db.init_app(app) 
    
   

    from .views import views
    from .auth import auth
    from .models import User, Note
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    

    createDatabase(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.Login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
            return User.query.get(int(id))

    return app

 
def createDatabase(app):
    with app.app_context():
        db_path = path.abspath(f"website/{DB_NAME}")  
        
        if not path.exists("website"): 
            path.makedirs("website")
            print("Created 'website' directory.")

        if path.exists(db_path):
            print("Database already exists at:", db_path)
        else:
            db.create_all()
            print("Database is created at:", db_path)





