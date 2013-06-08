
#### NDB TEST VIEW ########

"""
Complete working snippet of code which involves NDB datastore access.
/ndbindex:
    Lists out all the users logged in

/ndblogin
    Allows a new user to log in

/ndbfind
    Allows someone to find if a user with provided username is present in DB or not
    Prints 'present' if username present in database/datastore, or absent if not.
    
models.py contains:
    class DBTestingModel(ndb.Model):
        username = ndb.StringProperty(required=True)
        password = ndb.StringProperty(required=True)
        timestamp = ndb.DateTimeProperty(auto_now_add=True)

urls.py contains:
    app.add_url_rule('/ndblogin', 'ndblogin', view_func=views.ndblogin, methods=['GET', 'POST'])
    app.add_url_rule('/ndbfind', 'ndbfind', view_func=views.ndbfind, methods=['GET', 'POST'])
    app.add_url_rule('/ndbindex', 'ndbindex', view_func=views.ndbindex)

Also, need to add this import to make the following code work.
    from models import DBTestingModel


"""


def ndbindex():
    persons = DBTestingModel.query().fetch()
    ansstring = 'Users who logged into this snippet:<br> '
    for person in persons:
        ansstring += '(' + person.username + ', ' + person.password + ')<br>'
    return ansstring

def ndbfind():
    if request.method == 'POST':
        #NOTE(rushiagr): present is a list
        present = DBTestingModel.gql("WHERE username = :uname", uname=request.form['username']).fetch()
        #NOTE(rushiagr): the following commented line explains how to write the same query using NDB model query
        #present = NDBModel.query(NDBModel.username == request.form['username']).fetch()
        if present and present[0].username == request.form['username']:
            return 'present'
        return 'absent'
    else:
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Find>
            </form>                
                '''

def ndblogin():
    if request.method == 'POST':
        person = DBTestingModel(
            username = request.form['username'],
            password = request.form['password']
        )
        person.put()
        return redirect('ndbindex')
    else:
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        '''
        

