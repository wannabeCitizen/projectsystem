"""
For Handling all the db calls
"""
import json
import datetime

from lib.model import *


#<----- User Utilities

#Returns a single user based on google oauth token
def get_user(g_token):
	my_user = User.objects(token=g_token)
	user_str = my_user.to_json()
	data = json.loads(user_str)
	return data 

def create_user(name, address, token):
	current_time = datetime.datetime.now()
	new_user = User(name=name, email=address, token=token, join_on=current_time)

def delete_user():

def update_user():

#------>

#<----- Organization Utilities

def get_org(org_id):
	my_org = Organization.objects(unique=org_id)
	org_str = my_org.to_json()
	data = json.loads(org_str)
	return data 

def delete_org():

def create_org():

def update_org():


#--------->

#<------- Idea Utilities

def create_idea(org_id, idea_id):
	my_idea = Organization.objects(unique=org_id)
	org_str = my_org.to_json()
	data = json.loads(org_str)
	return data 

def get_idea(org_id, idea_id):


def delete_idea():

def update_idea():

#--------->


	