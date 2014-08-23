from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask.ext import restful
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin

from resources.organization import Organization, AllOrgs, Organization, OrgMember, OrgOwner

from mongoengine import connect

app = Flask(__name__)
api = restful.Api(app)
#google_login = GoogleLogin(app)

connect('projectsystem')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def devIndex():
    return render_template('devIndex.html')

#Here is an example of how you add an API resource to the app
#Simply pass the restful resource class and then the URL(s)
#Expected variables are placed in carrot brackets with a type declaration
api.add_resource(AllOrgs, '/api/org')
api.add_resource(Organization, '/api/org/<string:org_id>')
api.add_resource(OrgMember, '/api/org/<string:org_id>/member')
api.add_resource(OrgOwner, '/api/org/<string:org_id>/owner')


"""

Eventually we will need to get everything set with GoogleOAuth
Let's do this after we get the base API working and are happy.

#Taken from http://pythonhosted.org/Flask-GoogleLogin/
#Change once we start working on users
@app.route('/login')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
    user = User.filter_by(google_id=userinfo['id']).first()
    if user:
        user.name = userinfo['name']
        user.avatar = userinfo['picture']
    else:
        user = User(google_id=userinfo['id'],
                    name=userinfo['name'],
                    avatar=userinfo['picture'])
    db.session.add(user)
    db.session.flush()
    login_user(user)
    return redirect(url_for('index'))

"""


if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
