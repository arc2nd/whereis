#!/usr/bin/env python

import os
import json
from functools import wraps

from flask import Flask, render_template, Response, redirect, url_for, request, session, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')

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
            return splash()
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
                    return redirect(url_for('user_login'))
                else:
                    session['logged_in'] = now
            else:
                session['timeout'] = 10 
        return f(*args, **kwargs)
    return decorated_function


@app.route('/splash', methods=['GET'])
def splash():
    return render_template('splash.html')

@login_required
@app.route('/set', methods=['GET'])
def set():
    return render_template('set_location.html')


@app.route('/whereis', methods=['GET'])
@app.route('/whereis/<name>', methods=['GET'])
def whereis(name=None):
    path = 'locations.json'
    if os.path.exists(path):
        with open(path, 'r') as fp:
            loc_dict = json.load(fp)
        if name:
            return render_template('person.html', loc=loc_dict[name])
        else:
            return render_template('people.html', names=loc_dict)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


