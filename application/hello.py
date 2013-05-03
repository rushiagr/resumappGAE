from flask import Flask, escape, session, request, redirect, url_for, render_template
import time
import exceptions

import os

app = Flask(__name__)

db = {
    'rushi': {'password': 'rushipass',
              'metadata': None,
              'activated': True,
              'email': 'rushi.agr@gmail.com'},
    'rushi2': {'password': 'rushipass2',
               'metadata': None,
               'activated': True,
               'email': 'rushi2email'}
}



@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not credentials_valid(request.form):
            return 'Incorrect login'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if username_or_email_already_exists(request.form):
            return "We've detected an account with the credentials already present. Please login in such case"
        else:
            register_new_user(request.form)
            print 'registered new user'
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p>username<input type=text name=username>
            <p>password<input type=password name=password>
            <p>email<input type=email name=email>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route('/profile/<user>')
def profile_visit_handler(user):
    if not user_exists(user):
        return page_404()
    else:
        if is_logged_in():
            if user == logged_user():
                return full_profile(user)
        return public_profile(user)

############# All the fakes here #################

def register_new_user(form):
    username = form.get('username', None)
    password = form.get('password', None)
    email = form.get('email', None)
    db[username] = {'password': password,
                    'metadata': None,
                    'email': email}

def username_or_email_already_exists(form):
    if form['username'] in db:
        return True
    for user in db:     # Scope for optimization
        if db[user]['email'] == form.get('email', None):
            return True
    return False

def credentials_valid(form):
    username = form['username']
    password = form['password']
    if username in db and db[username]['password'] == password:
        return True
    return False

def is_logged_in():
    """Returns true if a user is logged in, else false."""
    return 'username' in session

def logged_user():
    """Returns the username of the logged-in user."""
    if is_logged_in():
        return session['username']
    else: raise exception


def login_form():
    login_str = '''
    login form:
    
    <form action='' method='post'>
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    '''

def full_profile(user):
    return 'full profile of user %s' % user

def public_profile(user):
    return 'public profile of user %s' % user

def user_exists(user):
    if db_user_exists(user):
        return True
    return False

def page_404():
    return 'this page does not exist'

###### All Database methods here #####

def db_user_exists(user):
    return user in db

def db_get_pass_for_user(user):
    return db[user]['password']

if __name__ == "__main__":
    app.secret_key = str(os.urandom(32))
    app.run(debug=True)
