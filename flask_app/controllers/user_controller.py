import re
from flask import render_template, request, redirect, session, flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

### THIS IS THE BASE ROUTE
@app.route('/')
def index():
    return render_template ('login.html')

### VALIDATE REGISTER ROUTE
@app.route('/register', methods=['POST'])
def register_user():

    query_data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        'password': request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }

    if User.validate_registration(query_data):
        pw_hash = bcrypt.generate_password_hash(query_data['password'])
        query_data['password'] = pw_hash
        del query_data['confirm_password']
        new_user_id = User.register_user (query_data)
        session['user_id'] = new_user_id
        return redirect ('/dashboard')

    return redirect('/')

    # collect data

    # run query (add user to data) and make user id into a variable you can track in session

    # log user in (via session)

    # redirect to wherever user goes after filling out form

### PROCESS LOGIN ROUTE

@app.route('/login', methods=['POST'])
def login():
    # check if user exists in database
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    # if user is not in database (i.e., not registered), don't validate and return user to login html
    if not user_in_db:
        flash ('Invalid Email or Password')
        return redirect ('/')
    # if password given doesn't match password in database, don't validate and return to user to login html
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ('Invalid Email or Password')
        return redirect ('/')

    # if given password matches password in database, log user in and set user_id into session
    session['user_id'] = user_in_db.id
    # redirect successfully logged in user to dashboard
    return redirect ('/dashboard')


### DASHBOARD ROUTE
@app.route('/dashboard')
def success():

    # query_data = {
    #     'user_id' : session['user_id']
    # }

    # user = User.get_by_id(query_data)
    
    if 'user_id' not in session:
        flash ('Please login or register to continue')
        return redirect('/')

    return render_template('success.html')

### LOGOUT ROUTE

@app.route ('/logout')
def logout():
    session.clear()
    return redirect ('/')


