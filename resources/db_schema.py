from flask.ext.restful import Resource, fields, marshal_with
from flask_login import LoginManager

project_fields = {
	"title": fields.String,
	"text" : fields.String,
	"short_desciption": fiels.String,
	"created_on": fields.DateTime,
	"budget": fields.Float,
	"owner": 1093824098 (User ID #)
	"organization": 2342345 (organization ID #)
	"members": [2340898, 920385, 23948084] (list of user ID #s)
	"complete": 0 (boolean on whether this project has been filed as completed)
	"base_node": 2341234324 (project ID # that is the base of this proposal or phase; if it is 0 then you know this is the root of the project or that it is a proposal)
	"phases": [2309840, 02983490, 203984098] List of other Project ID #s; if it is a proposal, this will be "None"]
	"next_phase": 902384098 (next chronological phase; if it is a proposal, this will be "None"; if it is the last phase of a project, we could have a placeholder like -1 or something)
	"vote_status": 0 [Has this been voted on?  This boolean will be reset if a new vote is awaiting]
    "to_do": [("fix JS", 098203498, 0), ("write overview", 08230984,1)]   (list of tuples for to-do items on this particular project or phase and who is the lead for each item, and whether it is done)
}

class Project(restful.Resource):

	@marshal_with(project_fields)
	@login_required
	def post(self):
		#will need to make db insert
		return project

	@marshal_with(project_fields)
	def get(self, id):
		#will need to do a db search
		return project

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return project

class Idea(restful.Resource):

	@marshal_with(idea_fields)
	@login_required
	def post(self):
		#will need to make db insert
		return idea

	@marshal_with(idea_fields)
	def get(self, id):
		#will need to do a db search
		return idea

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return idea

class User(restful.Resource):

	@marshal_with(user_fields)
	def post(self):
		#creating a user
		return user

	@marshal_with(idea_fields)
	@login_required
	def get(self, id):
		#will need to do a db search
		return user

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return user

class Proposal(restful.Resource):

	@marshal_with(proposal_fields)
	@login_required
	def post(self):
		#turn an idea into a proposal or start a proposal anew
		return proposal

	@marshal_with(proposal_fields)
	def get(self, id):
		#will need to do a db search
		return proposal

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return proposal

class Organization(restful.Resource):

	@marshal_with(org_fields)
	def post(self):
		#creating an organization
		return org

	@marshal_with(org_fields)
	@login_required
	def get(self, id):
		#will need to do a db search
		return org

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return org