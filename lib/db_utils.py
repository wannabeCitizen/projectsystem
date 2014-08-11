"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import User, Organization, MiniUser


#<----- User Utilities


#Returns a json-formatted single user based on google oauth token
def get_user(g_token):
    my_user = User.objects(token=g_token)
    user_str = my_user.first().to_json()
    data = json.loads(user_str)
    return data

def create_user(name, address, token):
    current_time = datetime.datetime.now()
    new_user = User(name=name, email=address, token=token, join_on=current_time)
    new_user.save()
    return new_user

def delete_user(token):
    old_user = User.objects(token=token)
    old_user.first().delete()
    return old_user

def update_user_rem(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"pull__%s" % k : kwargs[k])
     my_user.save()
    return my_user

def update_user_add(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"push__%s" % k : kwargs[k])
    my_user.save()
    return my_user

def update_user(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"set__%s" % k : kwargs[k])
    my_user.save()
    return my_user 

#------>

#<----- Organization Utilities

def get_org(org_id):
    my_org = Organization.objects(unique=org_id)
    org_str = my_org.first().to_json()
    data = json.loads(org_str)
    return data

def delete_org(org_id):
    old_org = Organization.objects(unique=org_id)
    old_org.first().delete()
    return old_org

def create_org(name, unique_id, owner):
    my_owner = User.objects(token=owner).first()
    new_mini = MiniUser(my_owner.name, my_owner.email, my_owner.token)
    new_org = Organization(name=name, unique=unique_id, owners=new_mini)
    new_org.save()
    return new_org

def update_org(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    my_org.update(**{"set__%s" % k : kwargs[k] for k in kwargs.keys()})
    return my_org

def update_org_rem(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    for k in kwargs.keys():
        my_org.update(**{"pull__%s" % k : kwargs[k])
    return my_org

def update_org_add(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    for k in kwargs.keys():
        my_org.update(**{"push__%s" % k : kwargs[k])
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
    old_idea.first().update(pull__ideas{'unique' : idea_id})
    return json.loads(old_idea.first().to_json())

def update_idea():
    pass

#--------->



