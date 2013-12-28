from contextlib import closing
import sqlite3
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash)
# from database.datatypes import Bill


app = Flask(__name__)
app.config.from_pyfile('billboy.cfg')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as fh:
            db.cursor().executescript(fh.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()
    

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    

@app.route('/')
def show_bills():
    cur = g.db.execute('SELECT date, name, amount, paid_by FROM bills '
                       'ORDER BY id DESC')
    bills = [dict(date=date, name=name, amount=amount, paid_by=paid_by)
             for date, name, amount, paid_by in cur.fetchall()]
    return render_template('show_bills.html', bills=bills)


@app.route('/add', methods=['POST'])
def add_bill():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO bills (date, name, amount, paid_by)'
                 'VALUES (?, ?, ?, ?)',
                 [request.form[key] for key in
                  ['date', 'name', 'amount', 'paid_by']])
    g.db.commit()
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
    init_db()
    app.run()
