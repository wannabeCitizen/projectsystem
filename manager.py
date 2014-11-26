from flask import session, redirect, url_for, escape, request, render_template
from flask_login import (login_required, login_user, logout_user,
                         current_user)

from app import app, api, googlelogin

from lib.model import User

from resources.organization import (OrganizationEP, OrgMember, OrgOwner,
                                    AllOrgs)
from resources.user import Login, AllUsers, UserEP, UserList
from resources.idea import (MetaIdea, VersionIdea, KarmaChange, IdeaComment,
                            IdeaReply, AllIdeas, FollowIdea)
from resources.project import (AllProjects, ProjectEP, ProjectMember, ProjectFollower,
                            ProjectRole, ProjectTask, ProjectVote, VoteBallot, Revision,
                            ProjectPhase, ProjectComment, ProjectReply)


from mongoengine import connect

import json
import sys

mongoIp = ((len(sys.argv) > 1) and sys.argv[1]) or 'localhost'
connect('projectsystem', host="mongodb://{}:27017/".format(mongoIp))

@googlelogin.user_loader
def load_user(userid):
    return User.objects(google_id=userid).first()


@app.route('/api/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def devIndex():
    return render_template('devIndex.html')

#Here is an example of how you add an API resource to the app
#Simply pass the restful resource class and then the URL(s)
#Expected variables are placed in carrot brackets with a type declaration
api.add_resource(AllUsers, AllUsers.url, AllUsers.url+'/')
api.add_resource(UserList, UserList.url, UserList.url+'/')
api.add_resource(UserEP, UserEP.url, UserEP.url+'/')
api.add_resource(Login, Login.url, Login.url+'/')

api.add_resource(AllOrgs, AllOrgs.url, AllOrgs.url+'/')
api.add_resource(OrganizationEP, OrganizationEP.url, OrganizationEP.url+'/')
api.add_resource(OrgMember, OrgMember.url, OrgMember.url+'/')
api.add_resource(OrgOwner, OrgOwner.url, OrgOwner.url+'/')

api.add_resource(AllIdeas, AllIdeas.url, AllIdeas.url+'/')
api.add_resource(MetaIdea, MetaIdea.url, MetaIdea.url+'/')
api.add_resource(VersionIdea, VersionIdea.url, VersionIdea.url+'/')
api.add_resource(KarmaChange, KarmaChange.url, KarmaChange.url+'/')
api.add_resource(IdeaComment, IdeaComment.url, IdeaComment.url+'/', IdeaComment.url2)
api.add_resource(IdeaReply, IdeaReply.url, IdeaReply.url+'/', IdeaReply.url2)
api.add_resource(FollowIdea, FollowIdea.url, FollowIdea.url+'/')

api.add_resource(AllProjects, AllProjects.url, AllProjects.url+'/')
api.add_resource(ProjectEP, ProjectEP.url, ProjectEP.url+'/')
api.add_resource(ProjectMember, ProjectMember.url, ProjectMember.url+'/')
api.add_resource(ProjectFollower, ProjectFollower.url, ProjectFollower.url+'/')
api.add_resource(ProjectRole, ProjectRole.url, ProjectRole.url+'/', ProjectRole.url1)
api.add_resource(ProjectTask, ProjectTask.url, ProjectTask.url+'/', ProjectTask.url1)
api.add_resource(ProjectVote, ProjectVote.url, ProjectVote.url+'/', ProjectVote.url1)
api.add_resource(VoteBallot, VoteBallot.url, VoteBallot.url+'/')
api.add_resource(Revision, Revision.url, Revision.url+'/')
api.add_resource(ProjectPhase, ProjectPhase.url, ProjectPhase.url+'/', ProjectPhase.url1)
api.add_resource(ProjectComment, ProjectComment.url, ProjectComment.url+'/', ProjectComment.url1)
api.add_resource(ProjectReply, ProjectReply.url, ProjectReply.url+'/', ProjectReply.url1)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', 5000)
