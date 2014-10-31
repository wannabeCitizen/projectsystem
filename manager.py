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
api.add_resource(AllUsers, '/api/user', '/api/user/')
api.add_resource(UserList, '/api/user/list','/api/user/list/')
api.add_resource(UserEP, '/api/user/<string:user_id>', '/api/user/<string:user_id>/')
api.add_resource(Login, '/api/login', '/api/login/')

api.add_resource(AllOrgs, '/api/org', '/api/org/')
api.add_resource(OrganizationEP, '/api/org/<string:org_id>', '/api/org/<string:org_id>/')
api.add_resource(OrgMember, '/api/org/<string:org_id>/member/<string:user_id>', '/api/org/<string:org_id>/member')
api.add_resource(OrgOwner, '/api/org/<string:org_id>/owner/<string:user_id>', '/api/org/<string:org_id>/owner')

api.add_resource(AllIdeas, AllIdeas.url, AllIdeas.url+'/')
api.add_resource(MetaIdea, MetaIdea.url, MetaIdea.url+'/')
api.add_resource(VersionIdea, VersionIdea.url, VersonIdea.url+'/')
api.add_resource(KarmaChange, KarmaChange.url, KarmaChange.url+'/')
api.add_resource(IdeaComment, IdeaComment.url, IdeaComment.url+'/')
api.add_resource(IdeaReply, IdeaReply.url, Idea.Reply.url+'/')
api.add_resource(FollowIdea, FollowIdea.url, FollowIdea.url+'/')

api.add_resource(AllProjects, '/api/org/<string:org_id>/project','/api/org/<string:org_id>/project/')
api.add_resource(ProjectEP, '/api/org/<string:org_id>/project/<string:project_id>','/api/org/<string:org_id>/project/<string:project_id>/')
api.add_resource(ProjectMember,'/api/org/<string:org_id>/project/<string:project_id>/member/<string:user_id>', '/api/org/<string:org_id>/project/<string:project_id>/member/<string:user_id>/' )
api.add_resource(ProjectFollower, '/api/org/<string:org_id>/project/<string:project_id>/follow', '/api/org/<string:org_id>/project/<string:project_id>/follow/')
api.add_resource(ProjectRole, '/api/org/<string:org_id>/project/<string:project_id>/role', '/api/org/<string:org_id>/project/<string:project_id>/role/')
api.add_resource(ProjectTask, '/api/org/<string:org_id>/project/<string:project_id>/task', '/api/org/<string:org_id>/project/<string:project_id>/task/')
api.add_resource(ProjectVote, '/api/org/<string:org_id>/project/<string:project_id>/vote', '/api/org/<string:org_id>/project/<string:project_id>/vote/')
api.add_resource(VoteBallot, '/api/org/<string:org_id>/project/<string:project_id>/ballot', '/api/org/<string:org_id>/project/<string:project_id>/ballot/')
api.add_resource(Revision, '/api/org/<string:org_id>/project/<string:project_id>/revision', '/api/org/<string:org_id>/project/<string:project_id>/revision/')
api.add_resource(ProjectPhase, '/api/org/<string:org_id>/project/<string:project_id>/phase', '/api/org/<string:org_id>/project/<string:project_id>/phase/')
api.add_resource(ProjectComment, '/api/org/<string:org_id>/project/<string:project_id>/comment', '/api/org/<string:org_id>/project/<string:project_id>/comment/')
api.add_resource(ProjectReply, '/api/org/<string:org_id>/project/<string:project_id>/comment/<string:comment_id>/reply', '/api/org/<string:org_id>/project/<string:project_id>/comment/<string:comment_id>/reply/')

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', 80)
