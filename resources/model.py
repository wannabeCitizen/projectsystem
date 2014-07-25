from mongoengine import *
import datetime


#Users are authenticated through Google OAuth - unsure how much more we should store
class User(Document):
	name = StringField(max_length=50, required=True)
	email = EmailField(required=True)
	unique = UUIDField(required=True)
	organizations = ListField(ReferenceField(Organization))
	projects = ListField(ReferenceField(Project))
	ideas = ListField(ReferenceField(Idea))
	joined_on = DateTimeField

	meta = {'allow_inheritance': True}

class MiniUser(EmbeddedDocument):
	name = StringField(required=True)
	email = EmailField(required=True)
	unique = UUIDField(required=True)


#Organizations are children of users
class Organization(Document):
	name = StringField(required=True)
	owners = ListField(ReferenceField(User))
	members = ListField(ReferenceField(User))
	short_description = StringField(max_length=400)



#Idea is the parent classe of project and proposals
class Idea(EmbeddedDocument):
	title = StringField(required=True)
	text = StringField(required=True)
	short_description(max_length=250)
	created_on = DateTimeField(default=datetime.datetime.now)
	#May want to consider a reverse_delete_rule for owner
	owner = ReferenceField(User) 
	organization = ReferenceField(Organization)
	members = ListField(ReferenceField(User))
	#we may want to consider how far down we store references to base_nodes
	base_node = ReferenceField(Idea, default='self') 
	karma = IntField

	meta = {'allow_inheritance': True}


class Vote(EmbeddedDocument):
	initiator = ReferenceField(User)
	quorum = DecimalField(min_value=.5, max_value=1.0)
	members = ListField(ReferenceField(User))
	description = StringField
	passed = BooleanField


class Proposal(Idea):
	budget = FloatField
	voted_on = BooleanField
	votes

	meta = {'allow_inheritance': True}

class Project(Proposal):
	complete = BooleanField
	#May want another Embedded Document?
	to_do = ListField(DictField)


