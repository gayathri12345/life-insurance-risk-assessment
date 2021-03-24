from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from App import routes, models    