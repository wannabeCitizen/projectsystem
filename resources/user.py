from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

from lib.db_utils import *

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


class UserEP(restful.Resource):
    def post(self):
        my_args = post_parser.parse_args()
        user = create_user(my_args['name'], my_args['email'], myargs['token'])
        return user

    #user_id will be an oauth token from google
    def get(self, user_id):
        user = get_user(user_id)
        return user

    def delete(self, user_id):
        delete_user(user_id)
        return 'user {id} is all gone'.format(id=user_id)

    def put(self):
        update_user()
        return user
