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
    new_project.current_rev = Revision(text=kwargs['text'], time=datetime.datetime.now)
    new_project.save()

    my_org.projects.append(new_project.minified)
    my_org.save()

    return json.loads(new_project.to_json())

def update_project(project_id, **kwargs):
    project_keys = ['title', 'short_description', 'budget','quorum','text']
    mini_keys = ['title', 'short_description']
    
    my_project = Project.objects.get(unique=project_id)
    current_time = datetime.datetime.now
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
        an_org.update_one(pull__projects__unique=project_id)
        an_org.update_one(push__projects=my_project.minified)

    my_project.last_edit = current_time
    my_project.save()

    ##Need to update mini
    return json.loads(my_project.to_json())

def get_idea(project_id):
    my_project = Project.objects.exclude('old_revs').get(unique=project_id)
    return json.loads(my_project.to_json())

def delete_project(user_id, org_id, project_id):
    old_project = Project.objects.get(unique=project_id)
    
    my_org = Organization.objects.get(unique=org_id)
    my_org.update(pull__projects__unique=project_id)
    my_org.update(push__del_projects= old_project)
    
    return json.loads(old_project.to_json())

def add_member(user_id, project_id):
    my_user = User.objects.get(google_id=user_id)

    my_project = Project.objects.get(unique=project_id)
    my_project.update(add_to_set__members=my_user.google_id)

    return my_user

def remove_member(user_id, project_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__members=user_id)

    return user_id

def add_follower(user_id, project_id):
    my_user = User.objects.get(google_id=user_id)

    my_project = Project.objects.get(unique=project_id)
    my_project.update(add_to_set__followers=my_user.google_id)

    return my_user

def remove_follower(user_id, project_id):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__followers=user_id)

    return user_id

def add_role(project_id, **kwargs):
    my_project = Project.objects.get(unique=project_id)
    my_role = Role(**kwargs)
    my_project.update(push__roles=my_role)

    return json.loads(my_role.to_json())

def remove_role(project_id, role_title):
    my_project = Project.objects.get(unique=project_id)
    my_project.update(pull__roles__role=role_title)

    return role_title

def update_role(project_id, **kwargs)



