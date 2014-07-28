from flask.ext.restful import Resource, fields
from flask_login import LoginManager

from manager import db

from resource.model import User, Organization

"""

For Future: 

Flask can do mandated parsing for us by setting requirements:

project_fields = {
	"title": fields.String,
	"text" : fields.String,
	"short_desciption": fiels.String,
	"created_on": fields.DateTime,
	"budget": fields.Float,
	...,
	...,
}

then simply add: 

@marshal_with(project_fields) to api resources that we want to 
restrict.

This allows us to keep private variables that never make it to the browser.


"""

class Project(restful.Resource):

	
	@login_required
	def post(self):
		#will need to make db insert
		return project

	def get(self, id):
		#will need to do a db search
		return project

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return project

class Idea(restful.Resource):

	@login_required
	def post(self):
		#will need to make db insert
		return idea

	def get(self, id):
		#will need to do a db search
		return idea

	def update(self, id):
		#will do an update command on mongo
		return idea

class User(restful.Resource):

	def post(self):
		#creating a user
		return user

	@login_required
	def get(self, id):
		#will need to do a db search
		return user

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return user

class Proposal(restful.Resource):

	@login_required
	def post(self):
		#turn an idea into a proposal or start a proposal anew
		return proposal

	def get(self, id):
		#will need to do a db search
		return proposal

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return proposal

class Organization(restful.Resource):

	def post(self):
		#creating an organization
		return org

	@login_required
	def get(self, id):
		#will need to do a db search
		return org

	@login_required
	def update(self, id):
		#will do an update command on mongo
		return org