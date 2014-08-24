from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask.ext import restful
from flask_login import (login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin

from lib.model import User

from resources.organization import Organization, OrgMember, OrgOwner, AllOrgs

from mongoengine import connect

import json
import datetime

app = Flask(__name__)
api = restful.Api(app)

app.config.update(
    SECRET_KEY='a3l2kfn93+09cn]diosu9fen[Nofo3indcMJdkjJDJ29',
    GOOGLE_LOGIN_CLIENT_ID='666333715586-orteiqqs7eq4h6he61epr2eg1fkm3e55.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='dF6S3MbnyHzP5WG9eBe1u_o0',
    GOOGLE_LOGIN_REDIRECT_URI='http://localhost:5000/oauth2callback')

googlelogin = GoogleLogin(app)

connect('projectsystem')

@googlelogin.user_loader
def load_user(userid):
    return User.objects(google_id=userid).first()


@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = User.objects(google_id=userinfo['id']).first()
    if not user:
        current_time = datetime.datetime.now()
        user = User(google_id=userinfo['id'], email=userinfo['email'], name=userinfo['name'], joined_on=current_time )
        user.save()

    login_user(user)
    return render_template('devIndex.html', json.loads(user.to_json()))   

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



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
