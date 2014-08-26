from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.db_utils import (get_org, get_all_ideas, delete_idea, create_idea,
                      update_org, match_ideas, add_follower)
from lib.verify import is_owner, is_in_org

import uuid
import json



class MetaIdea(restful.Resource):

    #Create a new version of an idea
    def post(self, org_id, idea_id):
        new_version_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            new_version_data['unique'] = str(uuid.uuid4())
            return create_version(current_user.google_id, idea_id, **new_version_data)
        else: 
            return abort(401, message="User not in org")

    #update a meta-idea
    def put(self, org_id, idea_id):
        new_data = request.get_json()
        verify = is_idea_owner(idea_id, current_user.google_id)
        if verify is True:
            return update_idea(idea_id, **new_data)
        else:
            return abort(401, message="User is not an owner")

    #get an individual idea
    def get(self, org_id, idea_id):
        return get_idea(idea_id)

    #remove an idea from the organization
    def delete(self, org_id, idea_id):
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            delete_idea(idea_id)
            return "Success"
        else: 
            return abort(401, "User is not an owner")

class FollowIdea(restful.Resource):

    #Add yourself as a follower
    def put(self, org_id, idea_id):
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            add_follower(current_user.google_id, idea_id)
            return "Success"
        else:
            return abort(401, "User not in organization")

    #Remove yourself as a follower
    def delete(self, org_id, idea_id):
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
            return match_ideas(search)
        else:
            return get_all_ideas(org_id)

    #Create a new meta-idea, check for version
    def post(self, org_id):
        print "made it"
        new_idea_data = request.get_json()
        print "got data"
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            new_idea_data['unique'] = str(uuid.uuid4())
            return create_idea(current_user.google_id, org_id, **new_idea_data)
        else: 
            return abort(401, message="User not in org")


