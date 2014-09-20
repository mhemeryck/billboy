import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


DEBUG = True
SECRET_KEY = 'development key'

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/billboy.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from app import models, views
from app.models import User


def init_users():
    """initialize users in db"""

    martijn = User('martijn', '0868599adbcee4fdd9283d9e90bc6887ee5d2319')
    katrien = User('katrien', 'e1416d1df89cc129117d73f27af3b47fcdd22a04')
    db.session.add(martijn)
    db.session.add(katrien)
    db.session.commit()
