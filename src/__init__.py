from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import json
import dotenv

dotenv.load_dotenv()

db = SQLAlchemy()
lm = LoginManager()

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + "/config.json"


def check_config():
    # Testing if config exists/any error in config
    try:
        with open(CONFIG_PATH, "r") as f:
            x = json.load(f)
            if not x:
                raise json.decoder.JSONDecodeError("lol", "1", 1)
    except FileNotFoundError:
        with open(CONFIG_PATH, "w") as f:
            x = {"installed": False}
            f.seek(0, 0)
            f.truncate(0)
            json.dump(x, f, indent=4)
    except json.decoder.JSONDecodeError:
        with open(CONFIG_PATH, "r") as f:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/config_backup.json", "w") as f2:
                f2.write(f.read())
        with open(CONFIG_PATH, "w") as f:
            x = {"installed": False,
                 "comment": "If you're seeing this, it means that the config file had errors in it. "
                            "The previous config has been saved as config_backup.json in the same "
                            "directory as the original config. Please correct your errors and try "
                            "again."}
            f.seek(0, 0)
            f.truncate(0)
            json.dump(x, f, indent=4)


check_config()


def create_app():
    app = Flask(__name__, static_folder="sad")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config.json") as f:
        app.config["INSTALLED"] = json.load(f).get("installed") or False
    app.secret_key = os.getenv("APP_SECRET_KEY") or "spanish inquisition"
    db.init_app(app)
    Migrate(app=app, db=db)
    lm.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()
        return app
