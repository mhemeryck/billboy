from datetime import datetime
from flask import (Flask, request, session, redirect, url_for, abort,
                   render_template, flash, jsonify)
from flask.ext.sqlalchemy import SQLAlchemy


DATABASE = '/tmp/billboy.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


class Bill(db.Model):

    """Shopping bill"""

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String)
    amount = db.Column(db.Float)
    paid_by = db.Column(db.Enum('katrien', 'martijn'))
    active = db.Column(db.Boolean, default=True)


@app.template_filter('datetime')
def format_datetime(value):
    return value.strftime('%Y-%m-%d')


@app.route('/')
def show_bills():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('bills.html', bills=Bill.query.all())


@app.route('/submit', methods=['POST'])
def submit_bill():
    if not session.get('logged_in'):
        abort(401)
    bill = Bill()
    bill.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    bill.description = request.form['description']
    bill.amount = request.form['amount']
    bill.paid_by = request.form['paid_by']
    db.session.add(bill)
    db.session.commit()
    flash('New bill successfully entered')
    return redirect(url_for('show_bills'))
    

@app.route('/update', methods=['POST'])
def update_bill():
    if not session.get('logged_in'):
        abort(401)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_bills'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_bills'))


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
