from mongoengine import *
import datetime


# Users are authenticated through Google OAuth - unsure how
# much more we should store
# Users only store most up-to-date versions of organizations,
# projects, and ideas

# A mini version of the user document to embed in other things



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
    #Google ID
    replier = StringField()
    text = StringField(required=True)
    time = DateTimeField(default=datetime.datetime.now())
    index = IntField()

class Comment(EmbeddedDocument):
    #Google ID
    commenter = StringField()
    text = StringField(required=True)
    time = DateTimeField(default=datetime.datetime.now())
    replies = ListField(EmbeddedDocumentField(Reply))
    num_replies = IntField()
    index = IntField()

class IdeaVersion(EmbeddedDocument):
    #Google ID
    thinker = StringField()
    text = StringField()
    unique = StringField(required=True)
    created_on = DateTimeField(required=True, default=datetime.datetime.now())
    last_edit = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

# Idea is the parent classe of project and proposals
class IdeaMeta(Document):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()
    created_on = DateTimeField(required=True, default=datetime.datetime.now())
    last_edit = DateTimeField(default=datetime.datetime.now())
    #This takes GoogleID
    created_by = StringField()
    
    followers = ListField(StringField())
    versions = ListField(EmbeddedDocumentField(IdeaVersion))
    comments = ListField(EmbeddedDocumentField(Comment))
    num_comments = IntField()
    minified = EmbeddedDocumentField(MiniIdea)
    my_org = EmbeddedDocumentField(MiniOrganization)
    karma = DictField()

    meta = {'allow_inheritance': True}


class Role(EmbeddedDocument):
    person = StringField(required=True)
    role = StringField()
    responsible_for = StringField()
    index = IntField()


class Task(EmbeddedDocument):
    index = IntField()
    #Google ID
    person = ListField(StringField())
    due = DateTimeField()
    complete = BooleanField()


class Phase(EmbeddedDocument):
    text = StringField(required=True)
    complete = BooleanField()
    tasks = ListField(IntField())
    goal_date = DateTimeField()
    index = IntField()


class Revision(EmbeddedDocument):
    text = StringField(required=True)
    time = DateTimeField(required=True, default=datetime.datetime.now())

class Ballot(EmbeddedDocument):
    voter = StringField()
    comment = StringField()
    in_favor = BooleanField()
    vote_id = IntField()


class Vote(EmbeddedDocument):
    #Google ID
    initiator = StringField()
    description = StringField()
    #empty to start; once verdict reached, can't delete?
    verdict = BooleanField()
    #All members added when initiated
    pending_votes = ListField(StringField())

    yay = ListField(EmbeddedDocumentField(Ballot))
    nay = ListField(EmbeddedDocumentField(Ballot))
    index = IntField()
    required_votes = IntField()

class MiniProject(EmbeddedDocument):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()

class Project(Document):
    title = StringField(required=True)
    unique = StringField(required=True)
    short_description = StringField()
    #This is an idea ID
    based_on = StringField()
    created_on = DateTimeField(required=True, default=datetime.datetime.now())
    last_edit = DateTimeField(default=datetime.datetime.now())
    #List of Google IDs
    members = ListField(StringField())
    followers = ListField(StringField())
    complete = BooleanField()
    budget = FloatField()
    majority = DecimalField(min_value=.5, max_value=1.0, precision=2)
    quorum = DecimalField(min_value=.5, max_value=1.0, precision=2, default=1.0)

    minified = EmbeddedDocumentField(MiniProject)
    my_org = EmbeddedDocumentField(MiniOrganization)

    votes = ListField(EmbeddedDocumentField(Vote))
    num_votes = IntField()
    
    roles = ListField(EmbeddedDocumentField(Role))
    num_roles = IntField(default=0)

    phases = ListField(EmbeddedDocumentField(Phase))
    num_phases = IntField()

    tasks = ListField(EmbeddedDocumentField(Task))
    num_tasks = IntField()

    old_revs = ListField(EmbeddedDocumentField(Revision))
    current_rev = EmbeddedDocumentField(Revision)

    comments = ListField(EmbeddedDocumentField(Comment))
    num_comments = IntField()


class User(Document):
    name = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    google_id = StringField(required=True)
    joined_on = DateTimeField(default=datetime.datetime.now())
    notifications = ListField(EmbeddedDocumentField(Notification))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.google_id)


# Organizations are parents of everything except users
class Organization(Document):
    name = StringField(required=True)
    unique = StringField(required=True)
    open_org = BooleanField(default=False)
    description = StringField(required=True)
    short_description = StringField(max_length=400)
    image = FileField()
    created_by = StringField()
    #owners and members have Google IDs
    owners = ListField(StringField())
    members = ListField(StringField())
    projects = ListField(EmbeddedDocumentField(MiniProject))
    del_projects = ListField(EmbeddedDocumentField(MiniProject))
    ideas = ListField(EmbeddedDocumentField(MiniIdea))
    pending_members = ListField(StringField())
    pending_owners = ListField(StringField())
    minified = EmbeddedDocumentField(MiniOrganization)

