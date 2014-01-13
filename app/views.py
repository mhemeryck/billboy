from datetime import datetime
import hashlib
import re
from flask import (request, session, redirect, url_for, abort, render_template,
                   flash)
from app import app, db
from app.models import Bill, User


def sha1(password):
    """calculate sha1 hash from password"""
    
    m = hashlib.sha1()
    m.update(password)
    return m.hexdigest()


def calculate_balances(year, month):
    """calculate current balances"""

    query = Bill.query.filter(Bill.active)
    
    names = ['katrien', 'martijn']
    amounts = {}
    for name in names:
        amounts[name] = 0
        for bill in query.filter_by(paid_by=name):
            if bill.date.month == month and bill.date.year == year:
                amounts[name] += bill.amount
    mean = sum([float(amounts[name]) for name in names]) / len(names)

    balances = {}
    for name in names:
        balances[name] = amounts[name] - mean
    return balances


@app.template_filter('datetime')
def format_datetime(value):
    return value.strftime('%Y-%m-%d')

@app.route('/<int:year>-<int:month>')
@app.route('/', defaults={'year': datetime.now().year,
                          'month': datetime.now().month})
def show_bills(year, month):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    query = Bill.query.filter(Bill.active)
    bills = []
    for bill in query:
        if bill.date.month == month and bill.date.year == year:
            bills.append(bill)
    balances = calculate_balances(year, month)
    return render_template('bills.html', bills=bills, balances=balances)


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
        query = User.query.filter_by(username=request.form['username'])
        if not query.count():
            flash('Invalid username', 'danger')
        else:
            user = query.first()
            if not user.password == sha1(request.form['password']):
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
