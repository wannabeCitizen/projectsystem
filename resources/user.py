from flask import request, session

from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse
from flask_login import login_user, make_secure_token, current_user

from lib.db_utils import get_user, delete_user, update_user, match_users
from lib.verify import is_owner, can_add
from lib.model import User, MiniUser

from app import googlelogin

import json
import datetime


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name',type=str,
    location='form', required=True,
    help='The user name',
)
post_parser.add_argument(
    'email',type=str,
    location='form', required=True,
    help='The user email address',
)
post_parser.add_argument(
    'token',type=str,
    location='form',
    help='The user oauth token',
)

update_parser = reqparse.RequestParser()
update_parser.add_argument(
    'task', type=str,
    location='args', 
    help='Figure out if its an add or removal',
)

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
        if not user:
            current_time = datetime.datetime.now()
            user = User(google_id=userinfo['id'], email=userinfo['email'], name=userinfo['name'], joined_on=current_time )
            user.minified = MiniUser(google_id=userinfo['id'], email=userinfo['email'], name=userinfo['name'])
            user.save()

        #Add user to the flask-login
        login_user(user, remember=True)      

        return json.loads(user.to_json())

class UserOrg(restful.Resource):
    #Get list of organizations user is part of
    def get(self):
        data = []
        for orgs in User.objects(google_id=current_user.google_id).first().organizations:
            new_org = json.loads(orgs.to_json())
            data.append(new_org)
        return data

class AllUsers(restful.Resource):

    #Returns all users matching a string
    def get(self, search):
        ten_users = match_users(search)
        return ten_users


class UserEP(restful.Resource):

    #user_id will be an oauth token from google
    def get(self, user_id):
        user = get_user(user_id)
        return user

    def delete(self, user_id):
        delete_user(user_id)
        return 'user {id} is all gone'.format(id=user_id)

    def put(self, user_id, update_type):
        new_data = request.form
        if update_type == 'remove':
            user = update_user_rem(user_id, **new_data)
        elif update_type == 'add':
            user = update_user_add(user_id, **new_data)
        else:
            user = update_user(user_id, **new_data)
        return user
