"""
For handling permission and verification requests
"""
import json
import datetime

from lib.model import User, Organization, MiniUser, MiniOrganization

#Checks if someone is an owner of an organization they are trying to modify
def is_owner(org_id, user_id):
	my_org = Organization.objects.get(unique=org_id)
	for users in my_org.owners:
		if users.google_id == user_id:
			return True
	return False

#Checks if the organization is open, if not, is the member allowed to do this?
def can_add(org_id, user_id):
	my_org = Organization.objects.get(unique=org_id)
	if my_org.open_org == True:
		return True
	else: 
		for users in my_org.owners:
			if users.google_id == user_id:
				return True
		return False