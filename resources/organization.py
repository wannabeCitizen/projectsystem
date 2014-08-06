from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

import bson

import json

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name',type=str, 
    location='form', required=True, 
    help='The organization name',
)
post_parser.add_argument(
    'description',type=str, 
    location='form', required=True, 
    help='The organization description',
)
post_parser.add_argument(
    'short_description',type=str, 
    location='form', 
    help='A short description for organization',
)
post_parser.add_argument(
	'owner', type=str,
	required=True, location='form',
	help='The user that owns the organization')


class Organization(restful.Resource):
	def post(self):
		my_args = post_parser.parse_args()
		user = get_user(my_args.owner)
		new_id = str(bson.objectid.ObjectId())
		organization = create_org()
		return organization

	def get(self, org_id):
		organization = get_org(org_id)
		return organization

	def delete(self, org_id):
		delete_org(org_id)
		return 'organization {id} is all gone'.format(id=org_id)

	def put(self):
		update_org()
		return organization


