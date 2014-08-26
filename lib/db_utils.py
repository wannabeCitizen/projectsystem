"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import (User, Organization, MiniUser, MiniOrganization, IdeaMeta, IdeaVersion,
                        MiniIdea)

from mongoengine import Q


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
        if minis.minified:
            data.append(json.loads(minis.minified.to_json()))
    return data

#Return all current app users
def get_all_users():
    data = []
    for users in User.objects:
        if users.minified:
            data.append(json.loads(users.minified.to_json()))
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

def add_idea(org_id, idea):
    my_org = Organization.objects.get(unique=org_id)
    my_org.update(push__ideas=idea)

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


def create_idea(creator, org_id, **kwargs):
    #Get my creator's object and my org
    my_owner = User.objects.get(google_id=creator)
    my_org = Organization.objects.get(unique=org_id)

    #Create object and set mini + creator + followers
    new_idea = IdeaMeta(**kwargs)
    new_idea.minified = MiniIdea(**kwargs)
    new_idea.created_by = my_owner.minified
    new_idea.followers = [my_owner.minified]
    new_idea.my_org = my_org.minified
    new_idea.num_comments = 0
    new_idea.save()

    my_owner.ideas.append(new_idea.minified)
    my_owner.save()

    my_org.ideas.append(new_idea.minified)
    my_org.save()

    return json.loads(new_idea.to_json())

def create_version(creator, idea_id, **kwargs):
    my_creator = User.objects.get(google_id=creator)

    new_version = IdeaVersion(**kwargs)
    new_version.thinker = my_creator.minified

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(push__versions=new_version)

    return json.loads(new_version.to_json())


def get_all_ideas(org_id):
    all_ideas = []
    my_org = Organization.objects.get(unique=org_id)
    for ideas in my_org.ideas:
        all_ideas.append(json.loads(ideas.to_json()))
    return all_ideas

def match_ideas(org_id, search_string):
    list_o_ideas = IdeaMeta.objects(Q(my_org__unique__exact=org_id) and (Q(title__icontains=search_string) | Q(short_description__icontains=search_string)))[:10]
    data = []
    for ideas in list_o_ideas:
        data.append(json.loads(ideas.to_json()))
    return data

def delete_idea(user_id, org_id, idea_id):
    old_idea = IdeaMeta.objects.get(unique=idea_id)
    
    
    my_org = Organization.objects.get(unique=org_id)
    my_org.ideas.update(pull__ideas__unique=idea_id)

    for people in old_idea.followers:
        my_user = User.objects.get(unique=people.google_id)
        my_user.update(pull__ideas__unique=idea_id)

    old_idea.delete()
    return json.loads(old_idea.to_json())


def update_idea(idea_id, **kwargs):
    idea_keys = ['title', 'short_description']

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    current_time = datetime.datetime.now
    for k in idea_keys:
        if k in kwargs.keys():
            my_idea.k = kwargs[k]
    my_idea.last_edit = current_time
    my_idea.save()
    return json.loads(my_idea.to_json())

def get_idea(idea_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    return json.loads(my_idea.to_json())

def add_follower(user_id, idea_id):
    my_user = User.objects.get(google_id=user_id)

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(push__followers=my_user.minified)

    my_user.update(push__ideas=my_idea.minified)

    return my_user

def remove_follower(user_id, idea_id):
    my_user = User.objects.get(google_id=user_id)
    my_user.update(pull__ideas__unique=idea_id)

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(pull__followers__unique=idea_id)

    return my_user

def update_version(idea_id, version_id, **kwargs):
    idea_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    for versions in my_idea.versions:
        if versions.unique == version_id:
            my_version = versions
    current_time = datetime.datetime.now
    for k in idea_keys:
        if k in kwargs.keys():
            my_version.k = kwargs[k]
    my_version.last_edit = current_time
    my_idea.save()
    return json.loads(my_idea.to_json())

def remove_version(idea_id, version_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.upate(pull__versions__unique=version_id)
    return my_idea

def change_karma(user_id, idea_id, version_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.karma[user_id] = version_id
    my_idea.save()
    return my_idea

def create_comment(user_id, idea_id, **kwargs):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_user = User.objects.get(google_id=user_id)
    my_index = my_idea.num_comments
    my_idea.update_one(inc__num_comments=1)

    my_comment = Comment(**kwargs)
    my_comment.my_order = my_index
    my_comment.num_replies = 0
    my_comment.time = datetime.datetime.now
    my_comment.commenter = my_user.minified

    my_idea.comments.append(my_comment)

    my_idea.save()
    return my_comment


def update_comment(idea_id, comment_id, **kwargs):
    comment_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_comment = my_idea.comments[comment_id]
    for k in comments_keys:
        if k in kwargs.keys():
            my_comment.k = kwargs[k]
    my_comment.time = datetime.datetime.now

    my_idea.save()

    return my_comment


def remove_comment(idea_id, comment_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.comments[comment_id] = None
    my_idea.save()

    return my_idea

def create_reply(user_id, idea_id, comment_id, **kwargs):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_user = User.objects.get(google_id=user_id)
    my_comment = my_idea.comments[comment_id]

    my_index = my_comment.num_replies
    mycomment.num_replies += 1

    my_reply = Reply(**kwargs)
    my_reply.my_order = my_index
    my_reply.time = datetime.datetime.now
    my_reply.replier = my_user.minified

    my_idea.comments[comment_id].replies.append(my_reply)

    my_idea.save()
    return my_reply


def update_reply(idea_id, comment_id, reply_id, **kwargs):
    reply_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_reply = my_idea.comments[comment_id].replies[reply_id]
    for k in reply_keys:
        if k in kwargs.keys():
            my_reply.k = kwargs[k]
    my_reply.time = datetime.datetime.now

    my_idea.save()

    return reply

def remove_reply(idea_id, comment_id, reply_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.comments[comment_id].replies[reply_id] = None
    my_idea.save()

    return my_idea


#--------->



