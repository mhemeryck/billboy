from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


DATABASE = '/tmp/billboy.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from app import models, views
