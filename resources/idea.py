from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse

import bson

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title',type=str, 
    location='form', required=True, 
    help='Title of Idea',
)
post_parser.add_argument(
    'text',type=str, 
    location='form', required=True, 
    help='Text of Idea - Markdown Renderable',
)
post_parser.add_argument(
    'short_description',type=str, 
    location='form', 
    help='A short description of the idea',
)
post_parser.add_argument(
    'org_id', type=str,
    location='form', required=True,
    help='the organization this idea is under')
post_parser.add_argument(
    'owner', type=str,
    location='form', required=True,
    help='the user posting this idea')
post_parser.add_argument(
    'base_node', type=str,
    location='form', 
    help='the idea this is a modifcation of')


class Idea(restful.Resource):
	def post(self):
		my_args = post_parser.parse_args()
        organization = my_args.org_id
        new_idea = str(bson.objectid.ObjectId())
		idea = create_idea()
		return idea

	def get(self, org_id, idea_id):
		idea = get_idea(org_id, idea_id)
		return idea

    def delete(self, org_id, idea_id):
        delete_idea(org_id, idea_id)
        return 'idea {id} is all gone'.format(id=idea_id)

    #This needs to be able to both modify an idea, add a user, and add karma
    #Need to think about more
    def put(self):
        update_idea()
        return idea
