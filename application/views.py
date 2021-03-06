"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, session, escape

from flask_cache import Cache

import logging

from google.appengine.ext import ndb

from application import app
from decorators import login_required, admin_required
from forms import ExampleForm
from models import ExampleModel, CredentialsModel, UserInfo, UserPersonalInfo, Education, Experience, Projects


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)




def index():
    if request.method == 'POST':
        user_email = request.form.get('inputEmail')
        user_password = request.form.get('inputPassword')

#        logging.critical(user_email, 'logged in')
        
        status = credentials_valid_and_user_registered(user_email, user_password)
        
        if status is False:
            flash('Incorrect login. Please try again.', 'error')
            return redirect(url_for('index'))

        return 'successful!'
#    if 'username' in session:
#        return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html')


def credentials_valid_and_user_registered(email, password):
    """
    Only returns true if the email exists in the datastore,
    and the password is correct.
    """
    #TODO(rushiagr): put all the server-side validation code here
    
    user = UserInfo.get_by_id(email)
    if user is not None and user.password == password:
        return True
    return False

def signup():
    if request.method == 'POST':
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        password_repeat = request.form.get('inputPasswordRepeat')
        
        if password != password_repeat:
            flash('Password not repeated exactly!', 'error')
            return redirect(url_for('signup'))
        
        if email_already_in_db(email):
            flash('Email already exists in our database!', 'error')
            return redirect(url_for('signup'))

        register_new_user(email, password)
        session['userEmail'] = email
        return redirect(url_for('dash'))

    elif request.method == 'GET':
        return render_template('signup.html')

def email_already_in_db(email):
    user = UserInfo.get_by_id(email)
    if user is not None:
        return True
    return False

def register_new_user(email, password):
    user = UserInfo(
        email=email,
        password=password,
        id=email
    )
    user.put()


def dash():
    if request.method == 'POST':
        #take data from form and put into database
        #TODO(rushiagr): do session expire check here
        user_personal_info = UserPersonalInfo(
            email=session.get('userEmail'),
            name=request.form.get('name'),
            title=request.form.get('position'),
            location=request.form.get('location'),
            summary=request.form.get('summary'),
        )
        user_personal_info.put()
        experience = Experience(
            email=session.get('userEmail'),
            position=request.form.get('experience_role'),
            description=request.form.get('experience_description'),
        )
        experience.put()
        projects = Projects(
            email=session.get('userEmail'),
            project_name=request.form.get('project_name'),
            description=request.form.get('project_description'),
        )
        projects.put()
        education = Education(
            email=session.get('userEmail'),
            duration=request.form.get('education_duration'),
            program=request.form.get('education_program'),
            institution=request.form.get('education_institution'),
            score_achieved=request.form.get('education_score'),
            score_out_of='10',
        )
        education.put()
        return render_template('profile.html',
                               session_user=session.get('userEmail'),
                               user_personal_info=user_personal_info,
                               experience=experience,
                               projects=projects,
                               education=education)
        
    elif request.method == 'GET':
        return render_template('edit_profile.html', session_user=session.get('userEmail'))


def login():
    if request.method == 'POST':
        logging.critical('ping1')
        trueorfalse = credentials_valid(request.form)
        logging.critical(trueorfalse)
        if trueorfalse is False:
#        if not credentials_valid(request.form):
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


def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



def profile_visit_handler(user):
    if not user_exists(user):
        return page_404()
    else:
        if is_logged_in():
            if user == logged_user():
                return full_profile(user)
        return public_profile(user)

    

def username_or_email_already_exists(form):
    username = CredentialsModel.gql("WHERE username = :uname",
                                    uname=form['username']).fetch()
    email = CredentialsModel.gql("WHERE email = :email",
                                    email=form['email']).fetch()
    logging.critical(username)
    logging.critical(email)
    if not username and not email:
        return False
#        logging.critical('returning false')
#    logging.critical('returning true')
    return True

def credentials_valid(form):
    logging.critical('pinga')
    v = CredentialsModel.gql("WHERE username = :uname AND password = :passwd",
                                 uname = form['username'],
                                 passwd = form['password']).fetch()
    logging.critical('pinga2')
#    username = form['username']
#    password = form['password']
#    if username in db and db[username]['password'] == password:
#        return True
#    return False
    if v:
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
    return_val = CredentialsModel.gql("WHERE username = :uname",
                                  uname=user)
    if not return_val:
        return False
    return True

#    return user in db

#def db_get_pass_for_user(user):
#    return db[user]['password']

#if __name__ == "__main__":
#    app.secret_key = str(os.urandom(32))
#    app.run(debug=True)








def home():
    return redirect(url_for('list_examples'))



def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


@login_required
def list_examples():
    """List all examples"""
    examples = ExampleModel.query()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name = form.example_name.data,
            example_description = form.example_description.data,
            added_by = users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key.id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def edit_example(example_id):
    example = ExampleModel.get_by_id(example_id)
    form = ExampleForm(obj=example)
    if request.method == "POST":
        if form.validate_on_submit():
            example.example_name = form.data.get('example_name')
            example.example_description = form.data.get('example_description')
            example.put()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
    return render_template('edit_example.html', example=example, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)
    try:
        example.key.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
        return redirect(url_for('list_examples'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_examples'))


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_examples():
    """This view should be cached for 60 sec"""
    examples = ExampleModel.query()
    return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

