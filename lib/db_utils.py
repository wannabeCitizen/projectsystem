"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import User, Organization, MiniUser, MiniOrganization


#<----- User Utilities


#Returns a json-formatted single user based on google oauth token
def get_user(user_id):
    my_user = User.objects.get(google_id=user_id)
    user_str = my_user.to_json()
    data = json.loads(user_str)
    return data


def delete_user(token):
    old_user = User.objects.get(google_id=token)
    old_user.delete()
    return old_user

def match_users(search_string):
    list_o_users = User.objects(name__icontains=search_string)[:10]
    data = []
    for minis in list_o_users:
        data.append(json.loads(minis.minified.to_json()))
    return data

#Return all current app users
def get_all_users():
    data = []
    for users in User.objects:
        data.append(json.loads(users.minified.to_json))
    return data



"""
Not in use:

def update_user_rem(token, **kwargs):
    my_user = User.objects.get(token=token)
    for k in kwargs.keys():
        my_user.update(**{"pull__%s" % k : kwargs[k]})
    return my_user

def update_user_add(token, **kwargs):
    my_user = User.objects(token=token).first()
    for k in kwargs.keys():
        my_user.update(**{"push__%s" % k : kwargs[k]})
    return my_user

def update_user(token, **kwargs):
    my_user = User.objects.get(google_id=token)
    for k in kwargs.keys():
        my_user.update(**{"set__%s" % k : kwargs[k]})
    return my_user
"""

#------>

#<----- Organization Utilities

def get_org(org_id):
    my_org = Organization.objects.get(unique=org_id)
    org_str = my_org.to_json()
    data = json.loads(org_str)
    return data

def get_all_orgs():
    all_orgs = []
    for orgs in Organization.objects.only('minified'):
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
    list_o_orgs = Organization.objects(name__icontains=search_string).only('minified')[:10]
    return json.loads(list_o_orgs.to_json())

def update_org(org_id, **kwargs):
    org_keys = ['name', 'open_org', "short_description", "description", 
                'image']

    my_org = Organization.objects.get(unique=org_id)
    for k in org_keys:
        if k in kwargs.keys():
            my_org.update(**{"set__%s" % k : kwargs[k]})
    return json.loads(my_org.to_json())

"""   
 Not in use:

def update_org_rem(org_id, **kwargs):
    my_org = Organization.objects.get(unique=org_id)
    for k in kwargs.keys():
        my_org.update(**{"pull__%s" % k : kwargs[k]})
    return my_org

def update_org_add(org_id, **kwargs):
    my_org = Organization.objects.get(unique=org_id)
    for k in kwargs.keys():
        my_org.update(**{"push__%s" % k : kwargs[k]})
    return my_org

"""

#--------->

#<--------- Idea Utilities


def create_idea(creator, **kwargs):
    my_owner = User.objects.get(google_id=creator)
    new_idea = IdeaMeta(**kwargs)
    new_idea.minified = MiniOrganization(**kwargs)
    new_org.created_by = my_owner.minified
    new_org.owners = [my_owner.minified]
    new_org.save()
    my_owner.organizations = [new_org.minified]
    my_owner.save()

def get_all_ideas(org_id):
    all_ideas = []
    my_org = Organization.objects(unique=org_id).only('ideas')
    for ideas in my_org.ideas:
        all_ideas.append(json.loads(ideas.to_json()))
    return all_ideas

def match_ideas(search_string):
    list_o_ideas = Organization.objects.only('ideas')(Q(ideas__title__icontains=search_string) | Q(ideas__text__icontains=search_string))[:10]
    data = []
    for ideas in list_o_ideas:
        data.append(json.loads(ideas.to_json()))
    return data

def delete_idea(idea_id):
    old_idea = Organization.objects.get(ideas__unique=idea_id)
    old_idea.update(pull__ideas={'unique' : idea_id})
    return json.loads(old_idea.first().to_json())

def update_idea():
    pass

#--------->



