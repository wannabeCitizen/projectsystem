from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import fields, reqparse
from lib.db_utils import (get_org, get_all_orgs, delete_org, create_org,
                      update_org)

import uuid

import json

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'name',type=str, 
    location='form', required=True, 
    help='The organization name',
)
post_parser.add_argument(
    'description',type=str, 
    location='form', required=True, 
    help='The organization description',
)
post_parser.add_argument(
    'short_description',type=str, 
    location='form', 
    help='A short description for organization',
)
post_parser.add_argument(
    'owner', type=str,
    required=True, location='form',
    help='The user that owns the organization')


class Organization(restful.Resource):
    def get(self, org_id):
        organization = get_org(org_id)
        return organization

    def delete(self, org_id):
        delete_org(org_id)
        return 'organization {id} is all gone'.format(id=org_id)

    def put(self, org_id, update_type):
        new_data = request.form   
        organization = update_org(org_id, **new_data)
        return organization

class AllOrgs(restful.Resource):
    def get(self):
        all_orgs = get_all_orgs()
        return all_orgs
    
    def post(self):
        new_org_data = request.get_json()
        #Eventuall will need to add an owner below
        # user = get_user(my_args.owner)
        new_org_data['unique'] = str(uuid.uuid4())
        organization = create_org(**new_org_data)
        return json.loads(organization.to_json())


class OrgMember(restful.Resource):
    def put(self, org_id):
        return "worked"

    def delete(self, org_id):
        return "worked"

class OrgOwner(restful.Resource):
    def put(self, org_id):
        return "worked"

    def delete(self, org_id):
        return "worked"


