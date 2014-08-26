from flask import session, redirect, url_for, escape, request, render_template
from flask_login import (login_required, login_user, logout_user,
                         current_user)

from app import app, api, googlelogin

from lib.model import User, MiniUser

from resources.organization import (OrganizationEP, OrgMember, OrgOwner, 
                                    AllOrgs)
from resources.user import Login, AllUsers, UserEP
from resources.idea import (MetaIdea, VersionIdea, KarmaChange, IdeaComment, 
                            ReplyComment, AllIdeas, FollowIdea)

from mongoengine import connect

import json


connect('projectsystem')

@googlelogin.user_loader
def load_user(userid):
    return User.objects(google_id=userid).first()


@app.route('/logout')
def logout():
    logout_user()
    return render_template('devIndex.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev')
def devIndex():
    return render_template('devIndex.html')

#Here is an example of how you add an API resource to the app
#Simply pass the restful resource class and then the URL(s)
#Expected variables are placed in carrot brackets with a type declaration
api.add_resource(AllOrgs, '/api/org')
api.add_resource(OrganizationEP, '/api/org/<string:org_id>')
api.add_resource(OrgMember, '/api/org/<string:org_id>/member/<string:user_id>', '/api/org/<string:org_id>/member')
api.add_resource(OrgOwner, '/api/org/<string:org_id>/owner/<string:user_id>', '/api/org/<string:org_id>/owner')
api.add_resource(Login, '/api/login')
api.add_resource(AllUsers, '/api/user')
api.add_resource(UserEP, '/api/user/<string:user_id>')
api.add_resource(AllIdeas, '/api/org/<string:org_id>/idea')
api.add_resource(MetaIdea, '/api/org/<string:org_id>/idea/<string:idea_id>')
api.add_resource(VersionIdea, '/api/org/<string:org_id>/idea/<string:idea_id>/version/<string:version_id>')
api.add_resource(KarmaChange, '/api/org/<string:org_id>/idea/<string:idea_id>/karma/<string:version_id>')
api.add_resource(IdeaComment, '/api/org/<string:org_id>/idea/<string:idea_id>/comment', '/api/org/<string:org_id>/idea/<string:idea_id>/comment/<int:comment_id>')
api.add_resource(ReplyComment, '/api/org/<string:org_id>/idea/<string:idea_id>/comment/<int:comment_id>/reply', '/api/org/<string:org_id>/idea/<int:idea_id>/comment/<string:comment_id>/reply/<int:reply_id>')
api.add_resource(FollowIdea, '/api/org/<string:org_id>/idea/<string:idea_id>/follow')



if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
