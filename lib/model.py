from mongoengine import *
import datetime


# Users are authenticated through Google OAuth - unsure how
# much more we should store
# Users only store most up-to-date versions of organizations,
# projects, and ideas

# A mini version of the user document to embed in other things
class MiniUser(EmbeddedDocument):
    name = StringField(required=True)
    email = EmailField(required=True)
    google_id = StringField(required=True)


class MiniOrganization(EmbeddedDocument):
    name = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField(max_length=400)

class Notification(EmbeddedDocument):
    pass

class MiniIdea(EmbeddedDocument):
    unique = UUIDField(required=True, binary=False)
    title = StringField(required=True)
    short_description = StringField(required=True)
 
class Reply(EmbeddedDocument):
    replier = EmbeddedDocumentField(MiniUser)
    text = StringField(required=True)
    time = DateTimeField(default=datetime.datetime.now)
    my_order = IntField()

class Comment(EmbeddedDocument):
    commenter = EmbeddedDocumentField(MiniUser)
    text = StringField(required=True)
    time = DateTimeField(default=datetime.datetime.now)
    replies = ListField(EmbeddedDocumentField(Reply))
    num_replies = IntField()
    my_order = IntField()

class IdeaVersion(EmbeddedDocument):
    thinker = EmbeddedDocumentField(MiniUser)
    text = StringField()
    unique = StringField(required=True)
    created_on = DateTimeField(required=True, default=datetime.datetime.now)
    last_edit = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

# Idea is the parent classe of project and proposals
class IdeaMeta(Document):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()
    created_on = DateTimeField(required=True, default=datetime.datetime.now)
    last_edit = DateTimeField(default=datetime.datetime.now)
    created_by = EmbeddedDocumentField(MiniUser)
    followers = ListField(EmbeddedDocumentField(MiniUser))
    versions = ListField(EmbeddedDocumentField(IdeaVersion))
    comments = ListField(EmbeddedDocumentField(Comment))
    num_comments = IntField()
    minified = EmbeddedDocumentField(MiniIdea)
    my_org = EmbeddedDocumentField(MiniOrganization)
    karma = DictField()

    meta = {'allow_inheritance': True}


class Role(EmbeddedDocument):
    pass


class Task(EmbeddedDocument):
    task = StringField(required=True)
    person = ListField(EmbeddedDocumentField(MiniUser))
    due = DateTimeField
    complete = BooleanField


class Phase(EmbeddedDocument):
    text = StringField
    complete = BooleanField
    tasks = ListField(EmbeddedDocumentField(Task))
    goal_date = DateTimeField


class Revision(EmbeddedDocument):
    text = StringField(required=True)
    time = DateTimeField(required=True)
    revision_of = UUIDField(required=True)

class Vote(EmbeddedDocument):
    initiator = EmbeddedDocumentField(MiniUser, required=True)
    description = StringField()
    verdict = BooleanField()
    vote_time = DateTimeField()
    pending_votes = ListField()
    completed_votes = ListField()
    toted_votes = IntField()
    required_votes = IntField()

    new_project = DynamicField()

class MiniProject(EmbeddedDocument):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()

class Project(Document):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()
    created_on = DateTimeField(required=True, default=datetime.datetime.now)
    last_edit = DateTimeField(default=datetime.datetime.now)
    members = ListField(EmbeddedDocumentField(MiniUser))
    followers = ListField(EmbeddedDocumentField(MiniUser))
    complete = BooleanField()
    budget = FloatField()
    voted_on = BooleanField()
    quorum = DecimalField(min_value=.5, max_value=1.0)

    minified = EmbeddedDocumentField(MiniProject)

    roles = ListField(EmbeddedDocumentField(Role))
    phases = ListField(EmbeddedDocumentField(Phase))
    tasks = ListField(EmbeddedDocumentField(Task))
    revisions = ListField(EmbeddedDocumentField(Revision))


class User(Document):
    name = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    google_id = StringField(required=True)
    organizations = ListField(EmbeddedDocumentField(MiniOrganization))
    projects = ListField(EmbeddedDocumentField(MiniProject))
    ideas = ListField(EmbeddedDocumentField(MiniIdea))
    joined_on = DateTimeField(default=datetime.datetime.now)
    notifications = ListField(EmbeddedDocumentField(Notification))
    minified = EmbeddedDocumentField(MiniUser)


    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.google_id)

class Proposal(EmbeddedDocument):
    pass

# Organizations are parents of everything except users
class Organization(Document):
    name = StringField(required=True)
    unique = StringField(required=True)
    open_org = BooleanField(default=False)
    description = StringField(required=True)
    short_description = StringField(max_length=400)
    image = FileField()
    created_by = EmbeddedDocumentField(MiniUser)
    owners = ListField(EmbeddedDocumentField(MiniUser))
    members = ListField(EmbeddedDocumentField(MiniUser))
    projects = ListField(EmbeddedDocumentField(MiniProject))
    ideas = ListField(EmbeddedDocumentField(MiniIdea))
    proposals = ListField(EmbeddedDocumentField(Proposal))
    pending_members = ListField(EmbeddedDocumentField(MiniUser))
    pending_owners = ListField(EmbeddedDocumentField(MiniUser))
    minified = EmbeddedDocumentField(MiniOrganization)

