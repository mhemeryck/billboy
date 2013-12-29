from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bill(db.Model):

    """Shopping bill"""

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    name = db.Column(db.String)
    amount = db.Column(db.Float)
    paid_by = db.Column(db.Enum('katrien', 'martijn'))
