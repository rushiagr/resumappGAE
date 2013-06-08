"""
models.py

App Engine datastore models


Tables:

UserInfo
    Email   string, unique, required(not null)
    Password    string, required(not null)
    Timestamp   datetime, autoadd
"""


from google.appengine.ext import ndb

class UserInfo(ndb.Model):
    """Class to keep user's email and password."""
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    



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
    