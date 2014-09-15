from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.verify import is_in_org, is_project_member, is_project_commenter, is_project_replier
from lib.project_utils import (create_project, update_project, get_project, delete_project,
                                add_follower, add_member, remove_member, remove_follower,
                                add_role, remove_role, update_role, add_task, update_task,
                                remove_task, add_vote, update_vote, remove_vote, cast_ballot,
                                get_revisions, add_phase, update_phase, remove_phase, create_comment,
                                update_comment, remove_comment, create_reply, update_reply, remove_reply,
                                match_projects, get_all_projects)

import uuid
import json


class AllProjects(restful.Resource):
    def post(self, org_id):
        new_project_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            new_project_data['unique'] = str(uuid.uuid4())
            return create_project(current_user.google_id, org_id, **new_project_data)
        else: 
            return abort(401, message="User not in org")

    def get(self, org_id):
        if 'search' in request.args and request.args['search'] != None:
            search = request.args['search']
            return match_projects(org_id, search)
        else:
            return get_all_projects(org_id)

class ProjectEP(restful.Resource):

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

    #remove an project from the organization
    def delete(self, org_id, project_id):
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            delete_project(current_user.google_id, org_id, project_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")

class ProjectMember(restful.Resource):
    #add a member to a project
    def put(self, org_id, project_id, user_id):
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            add_member(user_id, project_id)
            return "Success"
        else:
            return abort(401, message="User not in organization")

    def delete(self, org_id, project_id, user_id):
        verify = is_project_member(current_user.google_id, org_id)
        if verify is True:
            remove_member(user_id, project_id)
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

    #modify a role by resending the whole role object (rather than just the update) 
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
            return remove_role(project_id, old_role['index'])
        else:
            return abort(401, message="User is not on project")

class ProjectTask(restful.Resource):
    #add a task to a project
    def post(self, org_id, project_id):
        new_task = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return add_task(project_id, **new_task)
        else:
            return abort(401, message="User is not on project") 

    #modify a task  
    def put(self, org_id, project_id):
        task_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return update_task(project_id, **task_data)
        else:
            return abort(401, message="User is not on project")

    def delete(self, org_id, project_id):
        old_task = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)      
        if verify is True:
            return remove_task(project_id, old_task['index'])
        else:
            return abort(401, message="User is not on project")

class ProjectVote(restful.Resource):
    #add a vote to a project
    def post(self, org_id, project_id):
        new_vote = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            new_vote['initiator'] = current_user.google_id
            return add_vote(project_id, **new_vote)
        else:
            return abort(401, message="User is not on project") 

    #modify a vote  
    def put(self, org_id, project_id):
        vote_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return update_vote(project_id, **vote_data)
        else:
            return abort(401, message="User is not on project")

    #This should be disabled once testing is done
    def delete(self, org_id, project_id):
        old_vote = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)      
        if verify is True:
            return remove_vote(project_id, old_vote['index'])
        else:
            return abort(401, message="User is not on project")

class VoteBallot(restful.Resource):
    def put(self, org_id, project_id):
        vote_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return cast_ballot(project_id, **vote_data)
        else:
            return abort(401, message="User is not on project")

class Revision(restful.Resource):
    def get(self, org_id, project_id):
        return get_revisions(project_id)

class ProjectPhase(restful.Resource):
    #add a phase to a project
    def post(self, org_id, project_id):
        new_phase = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return add_phase(project_id, **new_phase)
        else:
            return abort(401, message="User is not on project") 

    #modify a phase
    def put(self, org_id, project_id):
        phase_data = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)
        if verify is True:
            return update_phase(project_id, **phase_data)
        else:
            return abort(401, message="User is not on project")

    def delete(self, org_id, project_id):
        old_phase = request.get_json()
        verify = is_project_member(current_user.google_id, project_id)      
        if verify is True:
            return remove_phase(project_id, old_phase['index'])
        else:
            return abort(401, message="User is not on project")

class ProjectComment(restful.Resource):

    #Add a new comment to a project
    def post(self, org_id, project_id):
        new_comment_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            create_comment(current_user.google_id, project_id, **new_comment_data)
            return "Success"
        else:
            return abort(401, message="Not in Organization")
             
    #Edit a comment
    def put(self, org_id, project_id):
        new_comment_data = request.get_json()
        comment_id = new_comment_data['index']
        verify = is_project_commenter(current_user.google_id, project_id, comment_id)
        if verify is True:
            update_comment(project_id, **new_comment_data)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")

    #remove comment and replies
    def delete(self, org_id, project_id):
        old_comment_data = request.get_json()
        comment_id = old_comment_data['index']
        verify = is_project_commenter(current_user.google_id, project_id, comment_id)
        if verify is True:
            remove_comment(project_id, comment_id)
            return "Success"
        else:
            return abort(401, message="Not Comment Owner")
        

class ProjectReply(restful.Resource):

    #Add a reply to a comment
    def post(self, org_id, project_id, comment_id):
        new_reply_data = request.get_json()
        verify = is_in_org(current_user.google_id, org_id)
        if verify is True:
            create_reply(current_user.google_id, project_id, comment_id, **new_reply_data)
            return "Success"
        else:
            return abort(401, message="Not in Organization")

    #Edit a reply to a comment
    def put(self, org_id, project_id, comment_id):
        new_reply_data = request.get_json()
        reply_id = new_reply_data['index']
        verify = is_project_replier(current_user.google_id, project_id, comment_id, reply_id)
        if verify is True:
            update_reply(project_id, comment_id, **new_reply_data)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")

    #Remove a reply
    def delete(self, org_id, project_id, comment_id):
        old_reply_data = request.get_json()
        reply_id = old_reply_data['index']
        verify = is_project_replier(current_user.google_id, project_id, comment_id, reply_id)
        if verify is True:
            remove_reply(project_id, comment_id, reply_id)
            return "Success"
        else:
            return abort(401, message="Not Reply Owner")


