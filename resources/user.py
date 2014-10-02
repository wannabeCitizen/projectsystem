from flask import request, session

from flask.ext import restful
from flask_login import login_user, make_secure_token, current_user
from flask.ext.restful import abort, reqparse

from lib.user_utils import get_user, delete_user, match_users, get_all_users, get_list
from lib.verify import is_owner, can_add
from lib.model import User

from app import googlelogin

import json
import datetime

# search_parser = reqparse.RequestParser()
# search_parser.add_argument('search', required=False, location='args')


class Login(restful.Resource):

    def post(self):
        #Grab code from authorization
        data = request.get_json()
        code = data['code']
        access_token = data['access_token']
        #Get redirect uri for next request
        redirect_uri = googlelogin.redirect_uri

        #Make token request
        #token = googlelogin.exchange_code(code, redirect_uri)


        userinfo = googlelogin.get_userinfo(access_token)

        #Check for user in DB
        user = User.objects(google_id=userinfo['id']).first()

        #If we don't know you, we add your ass
        #CHANGE THIS SHIT!
        if not user:
            current_time = datetime.datetime.now()
            user = User(google_id=userinfo['id'], email=userinfo['email'], name=userinfo['name'], joined_on=current_time )
            user.save()

        #Add user to the flask-login session (remember me auto-enabled)
        login_user(user)

        return json.loads(user.to_json())


class AllUsers(restful.Resource):

    #Returns all users matching a string
    def get(self):
        if 'search' in request.args and request.args['search'] != None:
            search = request.args['search']
            return match_users(search)
        elif request.args:
            abort(400, message="bad parameter")
        else:
            return get_all_users()

class UserList(restful.Resource):
    def post(self):
        data = request.get_json()
        return get_list(data)


class UserEP(restful.Resource):

    #user_id will be an oauth token from google
    def get(self, user_id):
        user = get_user(user_id)
        return user

    def delete(self, user_id):
        if current_user.google_id == user_id:
            delete_user(user_id)
            return "Success - User Deleted!"
        else:
            abort(401, message="Another user trying to delete this user")

