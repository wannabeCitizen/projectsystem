from mongoengine import *
import datetime


#Users are authenticated through Google OAuth - unsure how much more we should store
#Users only store most up-to-date versions of organizations, projects, and ideas
class User(Document):
	name = StringField(max_length=50, required=True)
	email = EmailField(required=True)
	token = StringField(required=True)
	organizations = ListField(EmbeddedDocument(MiniOrganization))
	projects = ListField(EmbeddedDocument(Project))
	ideas = ListField(EmbeddedDocument(Idea))
	joined_on = DateTimeField
	notifications = ListField(EmbeddedDocument(Notification))


#A mini version of the user document to embed in other things
class MiniUser(EmbeddedDocument):
	name = StringField(required=True)
	email = EmailField(required=True)
	unique = UUIDField(required=True)

class Notification(EmbeddedDocument):


#Organizations are parents of everything except users
class Organization(Document):
	name = StringField(required=True)
	unique = UUIDField(required=True, binary=False)
	description = StringField
	short_description = StringField(max_length=400)
	owners = ListField(EmbeddedDocument(MiniUser))
	members = ListField(EmbeddedDocument(MiniUser))
	projects = ListFiend(EmbeddedDocument(Project))
	ideas = ListField(EmbeddedDocument(Idea))
	proposals = ListField(EmbeddedDocument(Proposal))

class MiniOrganization(EmbeddedDocument)
	name = StringField(required=True)
	unique = UUIDField(required=True)
	short_description = StringField(max_length=400)


#Idea is the parent classe of project and proposals
class Idea(EmbeddedDocument):
	title = StringField(required=True)
	text = StringField(required=True)
	unique = UUIDField(required=True, binary=False)
	short_description(max_length=250)
	created_on = DateTimeField(required=True, default=datetime.datetime.now)
	last_edit = DateTimeField(default=datatime.datetime.now)
	#May want to consider a reverse_delete_rule for owner
	owner = EmbeddedDocument(MiniUser) 
	organization = EmbeddedDocument(MiniOrganization)
	followers = ListField(EmbeddedDocument(MiniUser))
	#we may want to consider how far down we store references to base_nodes
	base_node = EmbeddedDocument(Idea)
	karma = IntField

	meta = {'allow_inheritance': True}


class Vote(EmbeddedDocument):
	initiator = EmbeddedDocument(MiniUser, required=True)
	members = ListField(EmbeddedDocument(MiniUser), required=True)
	description = StringField
	verdict = BooleanField
	comments = StringField
	vote_time = DateTimeField


class Proposal(Idea):
	owner = EmbeddedDocument(MiniUser)
	budget = FloatField
	voted_on = BooleanField
	#always delete pending votes as they get counted
	pending_votes = ListField(EmbeddedDocument(Vote))
	completed_votes = ListField(EmbeddedDocument(Vote))
	votes = IntField
	quorum = DecimalField(min_value=.5, max_value=1.0)

	meta = {'allow_inheritance': True}

class Project(Proposal):
	complete = BooleanField
	phases = ListField(EmbeddedDocument)
	tasks = ListField(EmbeddedDocument(Tasks))
	revisions = ListField(EmbeddedDocument(Revision))

class Phase(EmbeddedDocument):
	text = StringField
	complete = BooleanField
	tasks = ListField(EmbeddedDocument(Tasks))
	goal_date = DateTimeField

class Tasks(EmbeddedDocument):
	task = StringField(required=True)
	person = ListField(EmbeddedDocument(MiniUser))
	due = DateTimeField
	complete = BooleanField

class Revision(EmbeddedDocument):
	text = StringField
	time = DateTimeField




