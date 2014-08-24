"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import User, Organization, MiniUser, MiniOrganization


#<----- User Utilities


#Returns a json-formatted single user based on google oauth token
def get_user(g_token):
    my_user = User.objects(google_id=g_token)
    user_str = my_user.first().to_json()
    data = json.loads(user_str)
    return data


def delete_user(token):
    old_user = User.objects(google_id=token)
    old_user.first().delete()
    return old_user

def update_user_rem(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"pull__%s" % k : kwargs[k]})
    return my_user

def update_user_add(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"push__%s" % k : kwargs[k]})
    return my_user

def update_user(token, **kwargs):
    my_user = User.objects(google_id=token).first()
    for k in kwargs.keys():
        my_user.update(**{"set__%s" % k : kwargs[k]})
    return my_user

#------>

#<----- Organization Utilities

def get_org(org_id):
    my_org = Organization.objects(unique=org_id)
    org_str = my_org.first().to_json()
    data = json.loads(org_str)
    return data

def get_all_orgs():
    all_orgs = []
    for orgs in Organization.objects:
        if orgs.minified:
            all_orgs.append(json.loads(orgs.minified.to_json()))
    return all_orgs

def delete_org(org_id):
    old_org = Organization.objects(unique=org_id)
    old_org.first().delete()
    return old_org

def create_org(creator, **kwargs):
    my_owner = User.objects(google_id=creator).first()
    new_org = Organization(**kwargs)
    new_org.minified = MiniOrganization(**kwargs)
    new_org.created_by = my_owner.minified
    new_org.owners = [my_owner.minified]
    new_org.save()
    my_owner.organizations = [new_org.minified]
    my_owner.save()
    return new_org

def add_member(org_id, user_id):
    my_org = Organization.objects(unique=org_id).first()
    my_user = User.objects(google_id=user_id).first()
    my_org.update(push__members=my_user.minified)
    my_user.update(push__organizations=my_org.minified)
    return my_user

def remove_member(org_id, user_id):
    my_org = Organization.objects(unique=org_id).first()
    my_user = User.objects(google_id=user_id).first()
    my_org.update(pull__members=my_user.minified)
    my_user.update(pull__organizations=my_org.minified)
    return my_user

def add_owner(org_id, user_id):
    my_org = Organization.objects(unique=org_id).first()
    my_user = User.objects(google_id=user_id).first()
    my_org.update(push__owners=my_user.minified)
    my_user.update(push__organizations=my_org.minified)
    return my_user

def remove_owner(org_id, user_id):
    my_org = Organization.objects(unique=org_id).first()
    my_user = User.objects(google_id=user_id).first()
    my_org.update(pull__owners=my_user.minified)
    my_user.update(pull__organizations=my_org.minified)
    return my_user

def update_org(org_id, **kwargs):
    org_keys = ['name', 'open_org', "short_description", "description", 
                'image']

    my_org = Organization.objects(unique=org_id).first()
    for k in org_keys:
        if k in kwargs.keys():
            my_org.update(**{"set__%s" % k : kwargs[k]})
    return json.loads(my_org.to_json())

def update_org_rem(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    for k in kwargs.keys():
        my_org.update(**{"pull__%s" % k : kwargs[k]})
    return my_org

def update_org_add(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    for k in kwargs.keys():
        my_org.update(**{"push__%s" % k : kwargs[k]})
    return my_org



#--------->

#<--------- Idea Utilities


def get_idea(idea_id):
    my_idea = Organization.objects(ideas__unique=idea_id)
    idea_str = my_idea.first().to_json()
    data = json.loads(idea_str)
    return data

def delete_idea(idea_id):
    old_idea = Organization.objects(ideas__unique=idea_id)
    old_idea.first().update(pull__ideas={'unique' : idea_id})
    return json.loads(old_idea.first().to_json())

def update_idea():
    pass

#--------->



