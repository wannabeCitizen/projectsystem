from flask import session, redirect, url_for, escape, request, render_template
from flask_login import (login_required, login_user, logout_user,
                         current_user)

from app import app, api, googlelogin

from lib.model import User, MiniUser

from resources.organization import Organization, OrgMember, OrgOwner, AllOrgs
from resources.user import Login

from mongoengine import connect

import json
import datetime



connect('projectsystem')

@googlelogin.user_loader
def load_user(userid):
    return User.objects(google_id=userid).first()


@app.route('/logout')
def logout():
    logout_user()
    return render_template('devIndex.html')


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
api.add_resource(Login, '/api/login')



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
