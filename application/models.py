"""
models.py

App Engine datastore models


Tables:

UserInfo
    Email   string, unique, required(not null)
    Password    string, required(not null)
    Timestamp   datetime, autoadd

UserPersonalInfo
    email string
    Name string
    Current_title string
    Summary Text (big text)
    
Experience
    email string
    Position            string
    Details_of_position text

Projects
    email string
    Project_in_one_line     string
    details of position     text

Education
    email string
    Duration    string
    Exam/Program    string
    Institution string
    Score   float

"""


from google.appengine.ext import ndb

class UserInfo(ndb.Model):
    """Class to keep user's email and password."""
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    




class UserPersonalInfo(ndb.Model):
    """Class to keep a user's personal info like name, title, etc."""
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    summary = ndb.TextProperty()

class Experience(ndb.Model):
    email = ndb.StringProperty(required=True)
    position = ndb.StringProperty(required=True)
    from_date = ndb.DateProperty()
    to_date = ndb.DateProperty()
    description = ndb.TextProperty()

class Projects(ndb.Model):
    email = ndb.StringProperty(required=True)
    project_name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    from_date = ndb.DateProperty()
    to_date = ndb.DateProperty()

class Education(ndb.Model):
    email = ndb.StringProperty(required=True)
    #TODO(rushiagr): make this work properly with dates
    #from_date = ndb.DateProperty(required=True)
    #to_date = ndb.DateProperty(required=True)
    duration = ndb.StringProperty(required=True)    #Temporary
    program = ndb.StringProperty(required=True)
    institution = ndb.StringProperty(required=True)
    score_achieved = ndb.StringProperty(required=True)
    score_out_of = ndb.StringProperty(required=True)


class ExampleModel(ndb.Model):
    """Example Model.
    
    Not used, just for some common understanding."""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

#This is also not used anywhere
class CredentialsModel(ndb.Model):
    """Saves all the user data: username, password and email."""
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    