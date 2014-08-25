from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.db_utils import (get_org, get_all_orgs, delete_org, create_org,
                      update_org)
from lib.verify import is_owner

import uuid
import json



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
