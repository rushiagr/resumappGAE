"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class CredentialsModel(ndb.Model):
    """Saves all the user data: username, password and email."""
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    
class DBTestingModel(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
