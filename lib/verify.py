"""
For handling permission and verification requests
"""
import json
import datetime

from lib.model import User, Organization, MiniUser, MiniOrganization

def is_owner(org_id, user_id):
	my_org = Organization.objects(unique=org_id).first()
	for users in my_org.owners:
		if users.google_id == user_id:
			return True
	return False