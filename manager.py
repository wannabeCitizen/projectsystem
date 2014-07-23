from flask import Flask, session, redirect, url_for, escape, request
from flask_googlelogin import GoogleLogin
from flask.ext import restful
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
api = restful.Api(app)
mongo = PyMongo(app)
google_login = GoogleLogin(app)

@app.route('/')
def index():
	render_template('index.html')

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

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == __main__:
	app.debug = True
	app.run()