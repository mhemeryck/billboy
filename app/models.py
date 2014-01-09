from datetime import datetime
from app import db


class User(db.model):
    
    """users to use the billboy app"""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String)
    pasword = db.Column(db.String(40))
    

class Bill(db.Model):

    """Shopping bill"""

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String)
    amount = db.Column(db.Float)
    paid_by = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
