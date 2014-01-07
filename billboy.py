from datetime import datetime
import re
from flask import (Flask, request, session, redirect, url_for, abort,
                   render_template, flash)
from flask.ext.sqlalchemy import SQLAlchemy


DATABASE = '/tmp/billboy.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


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
    return render_template('bills.html', bills=Bill.query.filter(Bill.active).all())


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
    flash('New bill successfully entered', 'success')
    return redirect(url_for('show_bills'))
    

@app.route('/edit', methods=['POST'])
def edit_bill():
    if not session.get('logged_in'):
        abort(401)
    pattern = re.compile('(?P<function>(delete|update))\[(?P<pk>(\d+))\]')
    match = pattern.match(request.form['btn'])
    if match is not None:
        bill_id = match.group('pk')
        bill = Bill.query.filter_by(id=bill_id).first()
        if match.group('function') == 'delete':
            bill.active = False
            flash('Successfully removed bill', 'success')
        elif match.group('function') == 'update':
            datestr = request.form['date[{}]'.format(bill_id)]
            bill.date = datetime.strptime(datestr, '%Y-%m-%d')
            bill.description = request.form['description[{}]'.format(bill_id)]
            bill.amount = request.form['amount[{}]'.format(bill_id)]
            bill.paid_by = request.form['paid_by[{}]'.format(bill_id)]
        db.session.add(bill)
        db.session.commit()
        flash('Successfully updated bill', 'success')
    return redirect(url_for('show_bills'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username', 'danger')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password', 'danger')
        else:
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('show_bills'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('show_bills'))


if __name__ == '__main__':
    db.create_all()
    app.run()
