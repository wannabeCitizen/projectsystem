from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.verify import is_owner, is_in_org, is_in_org, is_thinker, is_idea_owner, is_commenter, is_replier
from lib.idea_utils import (get_idea, get_all_ideas, delete_idea, create_idea,
                      update_idea, match_ideas, add_follower, create_version,
                      remove_follower, update_version, remove_version, change_karma,
                      create_comment, update_comment, remove_comment, create_reply,
                      update_reply, remove_reply)

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
            delete_idea(current_user.google_id, org_id, idea_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")

class FollowIdea(restful.Resource):

    #Add yourself as a follower
    def put(self, org_id, idea_id):
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            add_follower(current_user.google_id, idea_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

    #Remove yourself as a follower
    def delete(self, org_id, idea_id):
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            remove_follower(current_user.google_id, idea_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

class VersionIdea(restful.Resource):

    #Update a version of an idea
    def put(self, org_id, idea_id, version_id):
        new_data = request.get_json()
        verify = is_thinker(current_user.google_id, idea_id, version_id)
        if verify is True:
            update_version(idea_id, **new_data)
            return "Success"
        else:
            return abort(401, message="Not Owner of Idea")

    #remove a version of an idea
    def delete(self, org_id, idea_id, version_id):
        verify = is_thinker(current_user.google_id, idea_id, version_id)
        if verify is True:
            remove_version(idea_id, version_id)
            return "Success"
        else:
            return abort(401, message="Not Owner of Idea") 

class KarmaChange(restful.Resource):

    #Put Karma somewhere and remove it from elsewhere
    def put(self, org_id, idea_id, version_id):
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            change_karma(current_user.google_id, idea_id, version_id)
            return "Success"
        else:
            return abort(401, message="Not in Organization")
        

class IdeaComment(restful.Resource):

    #Add a new comment to a meta-idea
    def post(self, org_id, idea_id):
        new_comment_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            create_comment(current_user.google_id, idea_id, **new_comment_data)
            return "Success"
        else:
            return abort(401, message="Not in Organization")
             
    #Edit a comment
    def put(self, org_id, idea_id):
        new_comment_data = request.get_json()
        verify = is_commenter(current_user.google_id, idea_id, comment_id)
        if verify is True:
            update_comment(idea_id, **new_comment_data)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")

    #remove comment and replies
    def delete(self, org_id, idea_id):
        old_comment_data = request.get_json()
        comment_id = old_comment_data['index']
        verify = is_commenter(current_user.google_id, idea_id, comment_id)
        if verify is True:
            remove_comment(idea_id, comment_id)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")
        

class IdeaReply(restful.Resource):

    #Add a reply to a comment
    def post(self, org_id, idea_id, comment_id):
        new_reply_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            create_reply(current_user.google_id, idea_id, comment_id, **new_reply_data)
            return "Success"
        else:
            return abort(401, message="Not in Organization")

    #Edit a reply to a comment
    def put(self, org_id, idea_id, comment_id):
        new_reply_data = request.get_json()
        reply_id = new_reply_data['index']
        verify = is_replier(current_user.google_id, idea_id, comment_id, reply_id)
        if verify is True:
            update_reply(idea_id, comment_id, **new_reply_data)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")

    #Remove a reply
    def delete(self, org_id, idea_id, comment_id):
        old_reply_data = request.get_json()
        reply_id = old_reply_data['index']
        verify = is_replier(current_user.google_id, idea_id, comment_id, reply_id)
        if verify is True:
            remove_reply(idea_id, comment_id, reply_id)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")

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


