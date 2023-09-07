from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlite3 import OperationalError
import json
import os
from .constants import ESSENTIAL_CONFIG_KEYS

db = SQLAlchemy()
app = Flask(__name__)
csrf = CSRFProtect()


# def create_admin():

#     with app.app_context():
#         admin = None
#         try:
#             admin = User.query.filter_by(username='admin').first()
#         except Exception as e:
#             admin = None

#         if not admin:
#             heroes_path = os.path.join(app.config['UPLOAD_FOLDER'], 'admin')
#             Path(heroes_path).mkdir(parents=True, exist_ok=True)
#             admin_pw = generate_password_hash(app.config['ADMIN_PW'], method='sha256')
#             new_admin = User(username='admin', password=admin_pw, heroes_path=heroes_path, access_lvl=Level.ADMIN)
#             db.session.add(new_admin)
#             db.session.commit()
#         else:
#             # reset admin
#             heroes_path = os.path.join(app.config['UPLOAD_FOLDER'], 'admin')
#             Path(heroes_path).mkdir(parents=True, exist_ok=True)
#             admin.heroes_path = heroes_path
#             admin.password = generate_password_hash(app.config['ADMIN_PW'], method='sha256')
#             admin.access_lvl = Level.ADMIN
#             admin.email = ""
#             db.session.commit()

def is_config_valid(data: dict):
    for key in ESSENTIAL_CONFIG_KEYS:
        if key not in data:
            return key
    return None


def create_app(db_name="database.db"):
    # get abs path starting from this file location
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(basedir, db_name)
    config_dir = os.path.join(basedir, "..", "config.json")

    try:
        with open(config_dir, "r") as f:
            data = json.load(f)
            missing = is_config_valid(data)
            if missing: 
                raise ValueError(f"Config file not complete. Missing key: {missing}") 
            
            for key, val in data.items():
                if key == "UPLOAD_FOLDER":
                    # upload folder is [main.py-location]/[upload_folder]/
                    app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "..", val)
                else:
                    app.config[key] = val
                    
    except FileNotFoundError:
        raise FileNotFoundError("Create a config.json file in the main directory")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_dir
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # max incoming request size 16MB
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["JSON_AS_ASCII"] = False

    db.init_app(app)
    csrf.init_app(app)

    # include other flask routes and connect them
    from .views import views
    from .auth import auth
    # from .requests import req

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    # app.register_blueprint(req, url_prefix="/")

    # importing models for database creation
    from .models import User

    with app.app_context():
        db.create_all()

    # create_admin()

    login_manager = LoginManager()
    login_manager.login_view = (
        "auth.login"  # default page to call if user isn't logged in
    )
    login_manager.init_app(app=app)
    login_manager.login_message = ""

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
