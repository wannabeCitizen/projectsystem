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

def update_user(token, **kwargs):

    my_user = User.objects(token=token).first()
    my_user.update(**{"set__%s" % k : kwargs[k] for k in kwargs.keys()})
    my_user.save()
>>>>>>> b489d1ca4289ed1b0c6942254f137933815ccf30

#------>

#<----- Organization Utilities

def get_org(org_id):
    my_org = Organization.objects(unique=org_id)
    org_str = my_org.to_json()
    data = json.loads(org_str)
    return data

def delete_org(org_id):
    old_org = Organization.objects(unique=org_id)
    old_org.delete()
    return old_org


def create_org(name, unique_id, owner):
    my_owner = User(token=owner)
    new_mini = MiniUser(my_owner.name, my_owner.email, my_owner.token)
    new_org = Organization(name=name, unique=unique_id, owners=new_mini)


def update_org(org_id, **kwargs):
    my_org = Organization.objects(unique=org_id).first()
    my_org.update(**{"set__%s" % k : kwargs[k] for k in kwargs.keys()})
    my_org.save()


#--------->

#<------- Idea Utilities

def create_idea(org_id, idea_id):
   

def get_idea(org_id, idea_id):
    my_idea = Organization.objects(unique=org_id)
    org_str = my_org.to_json()
    data = json.loads(org_str)
    return data

<<<<<<< HEAD
=======
def get_idea(org_id, idea_id):
    pass


>>>>>>> b489d1ca4289ed1b0c6942254f137933815ccf30
def delete_idea():
    pass

<<<<<<< HEAD
def update_idea(**kwargs):
=======
def update_idea():
    pass
>>>>>>> b489d1ca4289ed1b0c6942254f137933815ccf30

#--------->



