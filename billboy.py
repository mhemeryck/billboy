from datetime import datetime
from flask import (Flask, request, session, redirect, url_for, abort,
                   render_template, flash)
from database import db, Bill


app = Flask(__name__)
app.config.from_pyfile('billboy.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
db.app = app
db.init_app(app)
db.create_all()


@app.template_filter('datetime')
def format_datetime(value):
    return value.strftime('%Y-%m-%d') #  babel.format_datetime(value, '%Y-%m-%d')


@app.route('/')
def show_bills():
    return render_template('show_bills.html', bills=Bill.query.all())


@app.route('/add', methods=['POST'])
def add_bill():
    if not session.get('logged_in'):
        abort(401)
    bill = Bill()
    bill.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    bill.name = request.form['name']
    bill.amount = request.form['amount']
    bill.paid_by = request.form['paid_by']
    db.session.add(bill)
    db.session.commit()
    flash('New bill successfully entered')
    return redirect(url_for('show_bills'))


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
    app.run()
