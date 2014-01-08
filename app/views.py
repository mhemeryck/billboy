from datetime import datetime
import re
from flask import (request, session, redirect, url_for, abort, render_template,
                   flash)
from app import app, db
from app.models import Bill


def calculate_balances():
    """calculate current balances"""

    query = Bill.query.filter(Bill.active)

    query_katrien = query.filter_by(paid_by='katrien')
    query_martijn = query.filter_by(paid_by='martijn')

    amount_katrien = sum([bill.amount for bill in query_katrien])
    amount_martijn = sum([bill.amount for bill in query_martijn])

    mean = float(amount_martijn + amount_katrien) / 2

    balances = {}
    balances['martijn'] = amount_martijn - mean
    balances['katrien'] = amount_katrien - mean
    return balances


@app.template_filter('datetime')
def format_datetime(value):
    return value.strftime('%Y-%m-%d')


@app.route('/')
def show_bills():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    bills = Bill.query.filter(Bill.active).all()
    balances = calculate_balances()
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
