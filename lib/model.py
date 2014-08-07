from mongoengine import *
import datetime


#Users are authenticated through Google OAuth - unsure how much more we should store
#Users only store most up-to-date versions of organizations, projects, and ideas

class MiniOrganization(EmbeddedDocument):
    name = StringField(required=True)
    unique = UUIDField(required=True)
    short_description = StringField(max_length=400)


class User(Document):
    name = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    token = StringField(required=True)
    organizations =
    ListField(EmbeddedDocumentField(MiniOrganization))
    projects = ListField(EmbeddedDocumentField(Project))
    ideas = ListField(EmbeddedDocumentField(Idea))
    joined_on = DateTimeField(default=datetime.datetime.now)
    notifications =
    ListField(EmbeddedDocumentField(Notification))


#A mini version of the user document to embed in other things
class MiniUser(EmbeddedDocument):
    name = StringField(required=True)
    email = EmailField(required=True)
    unique = UUIDField(required=True)

class Notification(EmbeddedDocument):
    pass


#Organizations are parents of everything except users
class Organization(Document):
    name = StringField(required=True)
    unique = UUIDField(required=True, binary=False)
    description = StringField
    short_description = StringField(max_length=400)
    owners = ListField(EmbeddedDocumentField(MiniUser))
    members = ListField(EmbeddedDocumentField(MiniUser))
    projects = ListField(EmbeddedDocumentField(Project))
    ideas = ListField(EmbeddedDocumentField(Idea))
    proposals = ListField(EmbeddedDocumentField(Proposal))


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
    followers = ListField(EmbeddedDocumentField(MiniUser))
    #we may want to consider how far down we store references to base_nodes
    base_node = EmbeddedDocument(Idea)
    karma = IntField

    meta = {'allow_inheritance': True}


class Vote(EmbeddedDocument):
    initiator = EmbeddedDocument(MiniUser, required=True)
    members = ListField(EmbeddedDocumentField(MiniUser), required=True)
    description = StringField
    verdict = BooleanField
    comments = StringField
    vote_time = DateTimeField


class Proposal(Idea):
    owner = EmbeddedDocument(MiniUser)
    budget = FloatField
    voted_on = BooleanField
    #always delete pending votes as they get counted
    pending_votes = ListField(EmbeddedDocumentField(Vote))
    completed_votes = ListField(EmbeddedDocumentField(Vote))
    votes = IntField
    quorum = DecimalField(min_value=.5, max_value=1.0)

    meta = {'allow_inheritance': True}

class Project(Proposal):
    complete = BooleanField
    phases = ListField(EmbeddedDocumentField)
    tasks = ListField(EmbeddedDocumentField(Tasks))
    revisions = ListField(EmbeddedDocumentField(Revision))

class Phase(EmbeddedDocument):
    text = StringField
    complete = BooleanField
    tasks = ListField(EmbeddedDocumentField(Tasks))
    goal_date = DateTimeField

class Tasks(EmbeddedDocument):
    task = StringField(required=True)
    person = ListField(EmbeddedDocument(MiniUser))
    due = DateTimeField
    complete = BooleanField

class Revision(EmbeddedDocument):
    text = StringField(required=True)
    time = DateTimeField(required=True)
    revision_of = UUIDField(required=True)




