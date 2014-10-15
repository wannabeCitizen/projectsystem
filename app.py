from flask import Flask
from flask.ext import restful
from flask_googlelogin import GoogleLogin

app = Flask(__name__)
api = restful.Api(app)

app.config.update(
    SECRET_KEY='a3l2kfn93+09cn]diosu9fen[Nofo3indcMJdkjJDJ29',
    GOOGLE_LOGIN_CLIENT_ID='666333715586-orteiqqs7eq4h6he61epr2eg1fkm3e55.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='dF6S3MbnyHzP5WG9eBe1u_o0',
    GOOGLE_LOGIN_REDIRECT_URI='http://projects.d0ck.me/dev/oauth2callback')

googlelogin = GoogleLogin(app)