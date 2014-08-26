"""
For Handling db calls on Organization Documents
"""
import json
import datetime

from lib.model import User, Organization, MiniUser, MiniOrganization
                        

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
    new_org.created_by = my_owner.minified
    new_org.owners = [my_owner.minified]
    new_org.save()
    my_owner.organizations = [new_org.minified]
    my_owner.save()
    return json.loads(new_org.to_json())

def add_member(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(add_to_set__members=my_user.minified)
    my_user.update(add_to_set__organizations=my_org.minified)
    return my_user

def remove_member(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(pull__members=my_user.minified)
    my_user.update(pull__organizations=my_org.minified)
    return my_user

def add_owner(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(add_to_set__owners=my_user.minified)
    my_user.update(add_to_set__organizations=my_org.minified)
    return my_user

def remove_owner(org_id, user_id):
    my_org = Organization.objects.get(unique=org_id)
    my_user = User.objects.get(google_id=user_id)
    my_org.update(pull__owners=my_user.minified)
    my_user.update(pull__organizations=my_org.minified)
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

    my_org = Organization.objects.get(unique=org_id)
    for k in org_keys:
        if k in kwargs.keys():
            my_org.update(**{"set__%s" % k : kwargs[k]})
    return json.loads(my_org.to_json())
