from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os
from flask_cors import CORS


app = Flask(__name__)
app.app_context().push()

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
DATABASE_URI = os.environ.get("UKULIMA")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI # "sqlite:///app.db"  # DATABASE_URI  #
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)

from API.endpoints import expenses, activities
