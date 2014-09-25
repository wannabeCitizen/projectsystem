"""
For handling permission and verification requests
"""
import json
import datetime

from lib.model import User, Organization, MiniOrganization, IdeaMeta, Project

#Checks if someone is an owner of an organization they are trying to modify
def is_owner(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    if user_id in my_org.owners:
        return True
    return False

#Checks if the organization is open, if not, is the member allowed to do this?
def can_add(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    if my_org.open_org == True:
        return True
    else:
        if user_id in  my_org.owners:
            return True
        return False

#Checks if user is in organization
def is_in_org(user_id, org_id):
    if is_owner(org_id, user_id):
        return True
    my_org = Organization.objects.get(unique=org_id)
    if user_id in my_org.members:
        return True
    return False

def is_idea_owner(idea_id, user_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    if my_idea.created_by == user_id:
        return True
    else:
        return False

def is_thinker(user_id, idea_id, version_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    for versions in my_idea.versions:
        if versions.unique == version_id:
            my_version = versions
    if my_version.thinker.google_id == user_id:
        return True
    else:
        return False

def is_commenter(user_id, idea_id, comment_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_commenter = my_idea.comments[comment_id].commenter
    if my_commenter == user_id:
        return True
    else:
        return False

def is_replier(user_id, idea_id, comment_id, reply_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_replier = my_idea.comments[comment_id].replies[reply_id].replier
    if my_replier == user_id:
        return True
    else:
        return False

def is_project_member(user_id, project_id):
    my_project = Project.objects.get(unique=project_id)
    if user_id in my_project.members:
        return True
    return False

def is_project_commenter(user_id, project_id, comment_id):
    my_project = Project.objects.get(unique=project_id)
    my_commenter = my_project.comments[comment_id].commenter.google_id
    if my_commenter == user_id:
        return True
    else:
        return False

def is_project_replier(user_id, project_id, comment_id, reply_id):
    my_project = Project.objects.get(unique=project_id)
    my_replier = my_project.comments[comment_id].replies[reply_id].replier.google_id
    if my_replier == user_id:
        return True
    else:
        return False
