"""
Utility for serializing objects with Relational References
into well-formatted JSON

This is a solution the way MongoEngine returns ReferenceFields

"""

import json

from lib.model import Organization, IdeaMeta, Project, User

org_fields = ['members', 'projects', 'created_by', 'owners', 'ideas', 
			'pending_members', 'pending_owners' ]

idea_fields = ['created_by', 'followers', 'my_org']

def serialize_org(org_object):
	final_data = json.loads(org_object.to_json())
	for fields in org_fields:
		data = org_object[fields]
		json_data = json.loads(data.to_json())
		final_data[fields] = json_data
	return final_data

def serialize_idea(idea_object):
	final_data = json.loads(idea_object.to_json())
	for fields in idea_fields:
		data = idea_object[fields]
		json_data = json.loads(data.to_json)
		final_data[fields] = json_data
	return final_data

def serialize_project(project_object):
	pass