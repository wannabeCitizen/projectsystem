"""
For Handling db calls on Ideas
"""
import json
import datetime

from lib.model import (User, Organization, MiniOrganization, IdeaMeta, IdeaVersion,
                        MiniIdea, Comment, Reply)

from mongoengine import Q

def create_idea(creator, org_id, **kwargs):
    #Get my creator's object and my org
    my_owner = User.objects.get(google_id=creator)
    my_org = Organization.objects.get(unique=org_id)

    #Create object and set mini + creator + followers
    new_idea = IdeaMeta(**kwargs)
    new_idea.minified = MiniIdea(**kwargs)
    new_idea.created_by = my_owner.google_id
    new_idea.followers = [my_owner.google_id]
    new_idea.my_org = my_org.minified
    new_idea.num_comments = 0
    new_idea.save()

    my_org.ideas.append(new_idea.minified)
    my_org.save()

    return json.loads(new_idea.to_json())

def create_version(creator, idea_id, **kwargs):
    my_creator = User.objects.get(google_id=creator)

    new_version = IdeaVersion(**kwargs)
    new_version.thinker = my_creator.google_id

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
    my_org.update(pull__ideas__unique=idea_id)

    old_idea.delete()
    return json.loads(old_idea.to_json())


def update_idea(idea_id, **kwargs):
    idea_keys = ['title', 'short_description']

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    current_time = datetime.datetime.now()
    for k in idea_keys:
        if k in kwargs.keys():
            my_idea.minified[k] = kwargs[k]
            my_idea[k] = kwargs[k]

    #Remember to do same for projects in the future!!
    my_orgs = Organization.objects(ideas__unique=idea_id)
    for an_org in my_orgs:
        an_org.update(pull__ideas__unique=idea_id)
        an_org.update(push__ideas=my_idea.minified)

    my_idea.last_edit = current_time
    my_idea.save()

    ##Need to update mini
    return json.loads(my_idea.to_json())

def get_idea(idea_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    return json.loads(my_idea.to_json())

def add_follower(user_id, idea_id):
    my_user = User.objects.get(google_id=user_id)

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(add_to_set__followers=my_user.google_id)

    return my_user

def remove_follower(user_id, idea_id):

    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(pull__followers=user_id)

    return user_id

def update_version(idea_id, version_id, **kwargs):
    idea_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    for versions in my_idea.versions:
        if versions.unique == version_id:
            my_version = versions
    current_time = datetime.datetime.now()
    for k in idea_keys:
        if k in kwargs.keys():
            my_version[k] = kwargs[k]
    my_version.last_edit = current_time
    my_idea.save()
    return json.loads(my_idea.to_json())

def remove_version(idea_id, version_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.update(pull__versions__unique=version_id)
    return my_idea

def change_karma(user_id, idea_id, version_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.karma[user_id] = version_id
    my_idea.save()
    return my_idea

def create_comment(user_id, idea_id, **kwargs):
    my_idea = IdeaMeta.objects.get(unique=idea_id)

    my_comment = Comment(**kwargs)
    my_comment.index = my_idea.num_comments

    my_idea.update(inc__num_comments=1)

    my_comment.num_replies = 0
    my_comment.time = datetime.datetime.now()
    my_comment.commenter = user_id

    my_idea.update(push__comments=my_comment)

    return json.loads(my_comment.to_json())


def update_comment(idea_id, **kwargs):
    comment_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_comment = my_idea.comments[kwargs['index']]
    for k in comment_keys:
        if k in kwargs.keys():
            my_comment[k] = kwargs[k]
    my_comment.time = datetime.datetime.now()

    my_idea.save()

    return json.loads(my_comment.to_json())


def remove_comment(idea_id, comment_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.comments[comment_id].text = "Comment removed by author."
    my_idea.save()

    return "Removed"

def create_reply(user_id, idea_id, comment_id, **kwargs):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_comment = my_idea.comments[comment_id]

    my_reply = Reply(**kwargs)
    my_reply.index = my_comment.num_replies
    my_comment.num_replies += 1
    my_reply.time = datetime.datetime.now()
    my_reply.replier = user_id

    my_idea.comments[comment_id].replies.append(my_reply)

    my_idea.save()
    return json.loads(my_reply.to_json())


def update_reply(idea_id, comment_id, **kwargs):
    reply_keys = ['text']
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_reply = my_idea.comments[comment_id].replies[kwargs['index']]
    for k in reply_keys:
        if k in kwargs.keys():
            my_reply[k] = kwargs[k]
    my_reply.time = datetime.datetime.now()

    my_idea.save()

    return json.loads(my_reply.to_json())

def remove_reply(idea_id, comment_id, reply_id):
    my_idea = IdeaMeta.objects.get(unique=idea_id)
    my_idea.comments[comment_id].replies[reply_id].text = "Reply removed by author."
    my_idea.save()

    return "Removed"