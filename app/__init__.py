import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

if DEBUG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/billboy.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from app import models, views
