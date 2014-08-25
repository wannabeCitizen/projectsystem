from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.db_utils import (get_org, get_all_ideas, delete_org, create_idea,
                      update_org, match_ideas)
from lib.verify import is_owner, is_in_org

import uuid
import json



class MetaIdea(restful.Resource):

    #Create a new version of an idea
    def post(self):
        pass

    #update a meta-idea
    def put(self):
        pass

    #get an individual idea
    def get(self):
        pass

    #remove an idea from the organization
    def delete(self):
        pass


class VersionIdea(restful.Resource):

    #Update a version of an idea
    def put(self):
        pass

    #remove a version of an idea
    def delete(self):
        pass

class KarmaChange(restful.Resource):

    #Put Karma somewhere and remove it from elsewhere
    def put(self):
        pass

class IdeaComment(restful.Resource):

    #Add a new comment to a meta-idea
    def post(self):
        pass

    #Edit a comment
    def put(self):
        pass

    #remove comment and replies
    def delete(self):
        pass

class ReplyComment(restful.Resource):

    #Add a reply to a comment
    def post(self):
        pass

    #Edit a reply to a comment
    def put(self):
        pass

    #Remove a reply
    def delete(self):
        pass

class AllIdeas(restful.Resource):

    #Get all meta-ideas or search by string
    def get(self, org_id):
        if 'search' in request.args and request.args['search'] != None:
            search = request.args['search']
            return match_ideas(org_id, search)
        else:
            return get_all_ideas(org_id)

    #Create a new meta-idea, check for version
    def post(self, org_id):
        new_idea_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            new_idea_data['unique'] = str(uuid.uuid4())
            return create_idea(current_user.google_id, org_id, **new_idea_data)
        else: 
            return abort(401, message="User not in org")


