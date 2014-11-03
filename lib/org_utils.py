"""
For Handling db calls on Organization Documents
"""
import json
import datetime

from lib.model import User, Organization, MiniOrganization, IdeaMeta
                        
from mongoengine import Q

def get_org(org_id):
    my_org = Organization.objects.get(unique=org_id)
    return json.loads(my_org.to_json())

def get_all_orgs():
    all_orgs = []
    for orgs in Organization.objects:
        if orgs.minified:
            all_orgs.append(json.loads(orgs.minified.to_json()))
    return all_orgs

def delete_org(org_id):
    old_org = Organization.objects.get(unique=org_id)
    old_org.delete()
    return old_org

def create_org(creator, **kwargs):
    my_owner = User.objects.get(google_id=creator)
    new_org = Organization(**kwargs)
    new_org.minified = MiniOrganization(**kwargs)
    new_org.created_by = my_owner.google_id
    new_org.owners = [my_owner.google_id]
    new_org.members = [my_owner.google_id]
    new_org.save()
    return json.loads(new_org.to_json())

def add_member(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(add_to_set__members=my_user.google_id)
    return my_user

def remove_member(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(pull__members=my_user.google_id)
    return my_user

def add_owner(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(add_to_set__owners=my_user.google_id)
    return my_user

def remove_owner(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(pull__owners=my_user.google_id)
    return my_user

def match_orgs(search_string):
    list_o_orgs = Organization.objects(name__icontains=search_string)[:10]
    data = []
    for minis in list_o_orgs:
        if minis.minified:
            data.append(json.loads(minis.minified.to_json()))
    return data

def update_org(org_id, **kwargs):
    org_keys = ['name', 'open_org', "short_description", "description", 
                'image']
    mini_keys = ['name', 'short_description']

    my_org = Organization.objects.get(unique=org_id)
    for k in org_keys:
        if k in kwargs.keys():
            my_org[k] = kwargs[k]
            my_org.update(**{"set__%s" % k : kwargs[k]})

    for k in mini_keys:
        if k in kwargs.keys():
            my_org.minified[k] = kwargs[k]
            my_org.update(**{"set__minified__%s" % k : kwargs[k]})

    # Will need to replicate this for projects when time comes!!
    my_ideas = IdeaMeta.objects(my_org=org_id)
    my_mini = my_org.minified
    for an_idea in my_ideas:
        an_idea.update(set__my_org=my_mini)


    return json.loads(my_org.to_json())
