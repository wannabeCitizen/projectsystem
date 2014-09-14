from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.verify import is_in_org, is_project_member
from lib.project_utils import create_project, update_project, get_project, delete_project,
                                add_follower, add_member, remove_member, remove_follower,
                                add_role, remove_role, update_role, 

import uuid
import json


class Project(restful.Resource):

	 def post(self, org_id):
        new_project_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            new_project_data['unique'] = str(uuid.uuid4())
            return create_project(current_user.google_id, org_id, **new_project_data)
        else: 
            return abort(401, message="User not in org")

    #update a project
    def put(self, org_id, project_id):
        new_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return update_project(project_id, **new_data)
        else:
            return abort(401, message="User is not an owner")

    #get an individual project
    def get(self, org_id, project_id):
        return get_project(project_id)

    #remove an idea from the organization
    def delete(self, org_id, project_id):
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            delete_project(current_user.google_id, org_id, idea_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")

class ProjectMember(restful.Resource):
	#add a member to a project
	def put(self, org_id, project_id, member):
		verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            add_member(new_member, project_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

	def delete(self, org_id, project_id, member):
		verify = is_project_member(current_user.google_id, org_id)
        if verify is True:
            remove_member(member, project_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

class ProjectFollower(restful.Resource):
	#add a follower to a project
	def put(self, org_id, project_id):
		verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            add_follower(current_user.google_id, project_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

	def delete(self, org_id, project_id):
		verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            remove_follower(current_user.google_id, project_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

class ProjectRole(restful.Resource):
	#add a Role to a project
	def post(self, org_id, project_id):
		new_role = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return add_role(project_id, **new_role)
        else:
            return abort(401, message="User is not on project") 

	#modify a role	
	def put(self, org_id, project_id):
		role_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return update_role(project_id, **role_data)
        else:
            return abort(401, message="User is not on project")

	def delete(self, org_id, project_id):
		old_role = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)		
        if verify is True:
            return remove_role(project_id, old_role[role])
        else:
            return abort(401, message="User is not on project")

class ProjectTask(restful.Resource):
	#add a task to a project
	def post(self, org_id, project_id):
		pass 

	#modify a task	
	def put(self, org_id, project_id):
		pass

	def delete(self, org_id, project_id):
		pass

class ProjectVote(restful.Resource):
	#add a vote to a project
	def post(self, org_id, project_id):
		pass 

	#modify a vote	
	def put(self, org_id, project_id):
		pass

	def delete(self, org_id, project_id):
		pass

class VoteBallot(restful.Resource):
	def put(self, org_id, project_id):
		pass

class Revision(restful.Resource):
	def get(self, org_id, projec_id):
		pass

class ProjectPhase(restful.Resource):
	#add a phase to a project
	def post(self, org_id, project_id):
		pass 

	#modify a phase	
	def put(self, org_id, project_id):
		pass

	def delete(self, org_id, project_id):
		pass

class ProjectComment(restful.Resource):

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
    def put(self, org_id, idea_id, comment_id):
        new_comment_data = request.get_json()
        verify = is_commenter(current_user.google_id, idea_id, comment_id)
        if verify is True:
            update_comment(idea_id, comment_id, **new_comment_data)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")

    #remove comment and replies
    def delete(self, org_id, idea_id, comment_id):
        verify = is_commenter(current_user.google_id, idea_id, comment_id)
        if verify is True:
            remove_comment(idea_id, comment_id)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")
        

class ProjectReply(restful.Resource):

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
    def put(self, org_id, idea_id, comment_id, reply_id):
        new_reply_data = request.get_json()
        verify = is_replier(current_user.google_id, idea_id, comment_id, reply_id)
        if verify is True:
            update_reply(idea_id, comment_id, reply_id, **new_reply_data)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")

    #Remove a reply
    def delete(self, org_id, idea_id, comment_id, reply_id):
        verify = is_replier(current_user.google_id, idea_id, comment_id, reply_id)
        if verify is True:
            remove_reply(idea_id, comment_id, reply_id)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")


