#!/usr/bin/env python

import os
import json
from functools import wraps

from flask import Flask, render_template, Response, redirect, url_for, request, session, flash

import config
import User

app = Flask(__name__)
app.secret_key = config.get_value('secret_key')


class Log(object):
    def log(self, msg):
        print(msg)

_log = Log()

def log_path():
    return


# Route decorators

def login_required(f):
    """ Ensure the user is logged in, send to login if not"""
    """Things to do to check and make sure a user is logged in
       1. check if session has a logged_in key, if not, send to splash page
       2. compare the current time to the last logged_in timestamp
          if the difference is greater than the timeout, send back to the login page
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # _log.log('login check', LogType.INFO)
        # check to see if we're logged in
        if 'logged_in' not in session:
            return user_login()
        else:
            # get the current time and see if it's more than the timeout greater
            #   than the last time a logged_in timestamp was stored
            #   if it's not store a new logged_in timestamp
            if 'timeout' in session:
                now = config.get_now()
                delta = session['timeout'] * 60 
                if now - session['logged_in'] > delta:
                    # _log.log('session timed out', LogType.INFO)
                    session.clear()
                    # return redirect(url_for('user_login'))
                else:
                    session['logged_in'] = now
            else:
                session['timeout'] = 10 
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
@login_required
def index():
    return whereis()
    # return render_template('index.html')


# user login
@app.route('/login', methods=['GET', 'POST'])
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    log_path()
    if(request.method == 'POST'):
        POST_USERNAME = str(request.form['user'])
        POST_PASSWORD = str(request.form['pwd'])

        result = User.User.GetByUsername(POST_USERNAME)

        if result and result.VerifyPassword(POST_PASSWORD):
            session['logged_in'] = config.get_now() 
            # session['user_id'] = result.id
            session['username'] = result.username
            session['role_id'] = result.role_id
            session['timeout'] = 10 
            _log.log('logged in')  # , LogType.INFO)
            flash('Success: You are now logged in', category='success')
        else:
            _log.log('bad credentials', LogType.WARN)
            flash('Warning: Username and/or password were incorrect', category='warning')

        return index()
    else:
        #form = UserAddForm()
        return render_template('user_login.html')  # , title='Log in')

# user logout
@app.route('/user/logout', methods=['GET'])
@login_required
def user_logout():
    log_path()
    if session.get('logged_in'):
        session.clear()
        _log.log('user logged out')  # , LogType.INFO)
    return user_login()

@app.route('/splash', methods=['GET'])
def splash():
    return render_template('splash.html')

@app.route('/set', methods=['GET', 'POST'])
@login_required
def set():
    if(request.method == 'POST'):
        location = str(request.form['location'])
        User.User.SetLocation(session['username'], location)
        print('you have just set your location to: {} '.format(location))
        return render_template('just_set.html', new_loc=location)
    return render_template('set_locations.html')


@app.route('/whereis', methods=['GET'])
@app.route('/whereis/<name>', methods=['GET'])
def whereis(name=None):
    all_users = User.User.GetAll()
    filter_users = {}
    for user in all_users:
        filter_users[user['username']] = user['location']
    if name:
        return render_template('person.html', name=name, loc=filter_users[name])
    else:
        return render_template('people.html', names=filter_users)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


