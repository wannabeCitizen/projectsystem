"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import User


#<----- User Utilities

#Returns a json-formatted single user based on google oauth token
def get_user(g_token):
    my_user = User.objects(token=g_token)
    user_str = my_user.to_json()
    data = json.loads(user_str)
    return data

def create_user(name, address, token):
    current_time = datetime.datetime.now()
    new_user = User(name=name, email=address, token=token, join_on=current_time)
    new_user.save()
    return new_user

def delete_user(token):
    old_user = User.objects(token=token)
    old_user.delete()
    return old_user

def update_user():
    pass

#------>

#<----- Organization Utilities

def get_org(org_id):
    my_org = Organization.objects(unique=org_id)
    org_str = my_org.to_json()
    data = json.loads(org_str)
    return data

def delete_org():
    pass

def create_org():
    pass


def update_org(**kwargs):
    pass


#--------->

#<------- Idea Utilities

def create_idea(org_id, idea_id):
    my_idea = Organization.objects(unique=org_id)
    org_str = my_org.to_json()
    data = json.loads(org_str)
    return data

def get_idea(org_id, idea_id):
    pass


def delete_idea():
    pass

def update_idea():
    pass

#--------->



