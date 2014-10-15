"""
For Handling db calls on Projects
"""
import json
import datetime

from lib.model import (User, Organization, MiniOrganization, Project, MiniProject, Vote,
                        Ballot, Role, Task, Phase, Revision)

from mongoengine import Q

def create_project(org_id, **kwargs):

    my_org = Organization.objects.get(unique=org_id)

    #Create project
    new_project = Project(**kwargs)
    new_project.minified = MiniProject(**kwargs)
    new_project.my_org = my_org.minified
    new_project.num_comments = 0
    new_project.current_rev = Revision(text=kwargs['text'], time=datetime.datetime.now())
    new_project.created_on = datetime.datetime.now()
    new_project.save()

    my_org.projects.append(new_project.minified)
    my_org.save()

    return json.loads(new_project.to_json())

def update_project(project_id, **kwargs):
    project_keys = ['title', 'short_description', 'based_on','budget','quorum','majority','text', 'complete']
    mini_keys = ['title', 'short_description']
    
    my_project = Project.objects.get(unique=project_id)
    for k in project_keys:
        if k in kwargs.keys():
            if k == 'text':
                old_rev = my_project.current_rev
                my_project.oldrevs.append(old_rev)
                my_project.current_rev = Revision(text=kwargs[k], time=current_time)
            elif k in mini_keys:
                my_project.minified[k] = kwargs[k]
                my_project[k] = kwargs[k]
            else:
                my_project[k] = kwargs[k]

    #Remember to do same for ideas in the future!!
    my_orgs = Organization.objects(projects__unique=project_id)
    for an_org in my_orgs:
        an_org.update(pull__projects__unique=project_id)
        an_org.update(push__projects=my_project.minified)

    my_project.last_edit = datetime.datetime.now()
    my_project.save()

    ##Need to update mini
    return json.loads(my_project.to_json())

def get_project(project_id):
    my_project = Project.objects.exclude('old_revs').get(unique=project_id)
    return json.loads(my_project.to_json())

def match_projects(org_id, search_string):
    list_o_projects = Project.objects(Q(my_org__unique__exact=org_id) and (Q(title__icontains=search_string) | Q(short_description__icontains=search_string)))[:10]
    data = []
    for projects in list_o_projects:
        data.append(json.loads(projects.to_json()))
    return data

def get_all_projects(org_id):
    all_projects = []
    my_org = Organization.objects.get(unique=org_id)
    for projects in my_org.projects:
        all_projects.append(json.loads(projects.to_json()))
    return all_projects

def delete_project(user_id, org_id, project_id):
    old_project = Project.objects.get(unique=project_id)
    old_project.delete()

    my_org = Organization.objects.get(unique=org_id)
    my_org.update(pull__projects__unique=project_id)
    
   #Eventually we'll want to enforce something stricter 
    # my_org = Organization.objects.get(unique=org_id)
    # my_org.update(pull__projects__unique=project_id)
    # my_org.update(push__del_projects= old_project)
    
    return json.loads(old_project.to_json())

def add_member(user_id, project_id):
    my_user = User.objects.get(google_id=user_id)

    my_project = Project.objects.get(unique=project_id)
    my_project.update(add_to_set__members=my_user.google_id)

    return json.loads(my_user.to_json())

def remove_member(user_id, project_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__members=user_id)

    return "Removed"

def add_follower(user_id, project_id):
    my_user = User.objects.get(google_id=user_id)

    my_project = Project.objects.get(unique=project_id)
    my_project.update(add_to_set__followers=my_user.google_id)

    return json.loads(my_user.to_json())

def remove_follower(user_id, project_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__followers=user_id)

    return user_id

def add_role(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_role = Role(**kwargs)
    my_role.index = my_project.num_roles
    my_project.update(inc__num_roles=1) 
    my_project.update(push__roles=my_role)

    return json.loads(my_role.to_json())

def remove_role(project_id, role_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.roles[role_id].removed = True
    my_project.save()

    return json.loads(my_project.roles[role_id].to_json())

def update_role(project_id, **kwargs):
    role_keys = ['person', 'role', 'responsible_for']

    my_project = Project.objects.get(unique=project_id)
    my_role = my_project.roles[kwargs['index']]

    for k in role_keys:
        if k in kwargs:
            my_role[k] = kwargs[k]

    my_project.last_edit = datetime.datetime.now()
    my_project.save()

    return json.loads(my_role.to_json())

def add_task(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_task = Task(**kwargs)
    my_task.index = my_project.num_tasks
    my_project.update(inc__num_tasks=1) 
    my_project.update(push__tasks=my_task)

    return json.loads(my_task.to_json())

def update_task(project_id, **kwargs):
    task_keys = ['person', 'due', 'complete', 'to_do']

    my_project = Project.objects.get(unique=project_id)
    my_task = my_project.tasks[kwargs['index']]

    for k in task_keys:
        if k in kwargs:
            my_task[k] = kwargs[k]

    my_project.last_edit = datetime.datetime.now()
    my_project.save()

    return json.loads(my_task.to_json())

def remove_task(project_id, task_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.task[task_id].removed = True
    my_project.save()

    return json.loads(my_project.tasks[task_id].to_json())

def add_vote(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_vote = Vote(**kwargs)
    my_vote.index = my_project.num_votes
    my_project.update(inc__num_votes=1) 

    q = my_project.quorum
    num_mem = len(my_project.members)
    my_vote.required_votes = int(round(q*num_mem))
    my_vote.pending_votes = my_project.members

    my_project.update(push__votes=my_vote)

    return json.loads(my_vote.to_json())

def update_vote(project_id, **kwargs):
    vote_keys = ['description']

    my_project = Project.objects.get(unique=project_id)
    my_vote = my_project.votes[kwargs['index']]

    for k in task_keys:
        if k in kwargs:
            my_vote[k] = kwargs[k]

    my_project.last_edit = datetime.datetime.now()
    my_project.save()

    return json.loads(my_vote.to_json())

def remove_vote(project_id, vote_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.votes[vote_id].removed = True
    my_project.save()

    return json.loads(my_project.votes[vote_id].to_json())

def cast_ballot(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_vote = my_project.votes[kwargs['index']]
    me = kwargs['voter']

    if kwargs['voter'] not in my_vote.pending_votes:
        return "Already Voted"

    my_ballot = Ballot(**kwargs) 
    
    if kwargs['in_favor']:
        my_vote.yay.append(my_ballot)
        my_vote.pending_votes.remove(me)
    else:
        my_vote.nay.append(my_ballot)
        my_vote.pending_votes.remove(me)

    my_project.save()

    return "Success"

def get_revisions(project_id):
    my_revs = Projects.objects.only('old_revs').get(unique=project_id)
    return json.loads(my_revs.to_json())

def add_phase(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_phase = Phase(**kwargs)
    my_phase.index = my_project.num_phases
    my_project.update(inc__num_tasks=1) 
    my_project.update(push__phases=my_phase)

    return json.loads(my_phase.to_json())

# Not sure if we need this:
# def get_phase(project_id, phase_id):
#     my_project = Project.objects.get(unique=project_id)
#     my_phase = my_project.phases[phase_id]

#     return json.loads(my_phase.to_json())

def update_phase(project_id, **kwargs):
    phase_keys = ['text', 'tasks', 'complete', 'goal_date']

    my_project = Project.objects.get(unique=project_id)
    my_phase = my_project.phases[kwargs['index']]

    for k in phase_keys:
        if k in kwargs:
            my_phase[k] = kwargs[k]

    my_project.last_edit = datetime.datetime.now()
    my_project.save()

    return json.loads(my_phase.to_json())

def remove_phase(project_id, phase_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__phases__index=phase_id)

    return "Removed"

def create_comment(user_id, project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)

    my_comment = Comment(**kwargs)
    my_comment.index = my_project.num_comments

    my_project.update(inc__num_comments=1)
    
    my_comment.num_replies = 0
    my_comment.time = datetime.datetime.now()
    my_comment.commenter = user_id

    my_project.update(push__comments=my_comment)

    return json.loads(my_comment.to_json())

def update_comment(project_id, **kwargs):
    comment_keys = ['text']
    my_idea = Project.objects.get(unique=project_id)
    my_comment = my_project.comments[kwargs['index']]
    for k in comments_keys:
        if k in kwargs.keys():
            my_comment[k] = kwargs[k]
    my_comment.time = datetime.datetime.now()

    my_idea.save()

    return json.loads(my_comment.to_json()) 

def remove_comment(project_id, comment_id):
    my_project = Project.objects.get(unique=idea_id)
    my_project.comments[comment_id].text = "Comment removed by author"
    my_project.save()

    return "Removed"

def create_reply(user_id, project_id, comment_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_comment = my_project.comments[comment_id]

    my_reply = Reply(**kwargs)
    my_reply.index = my_comment.num_replies
    my_comment.num_replies += 1
    my_reply.time = datetime.datetime.now()
    my_reply.replier = user_id

    my_project.comments[comment_id].replies.append(my_reply)

    my_project.save()
    return json.loads(my_reply.to_json())

def update_reply(project_id, comment_id, **kwargs):
    reply_keys = ['text']
    my_project = Project.objects.get(unique=project_id)
    my_reply = my_project.comments[comment_id].replies[kwargs['index']]
    for k in reply_keys:
        if k in kwargs.keys():
            my_reply[k] = kwargs[k]
    my_reply.time = datetime.datetime.now()

    my_project.save()

    return json.loads(my_reply.to_json())

def remove_reply(project_id, comment_id, reply_id):
    my_project = Project.objects.get(unique=project_id)
    my_reply = my_project.comments[comment_id].replies[reply_id].text = "Reply removed by author"
    my_project.save()

    return "Removed"
